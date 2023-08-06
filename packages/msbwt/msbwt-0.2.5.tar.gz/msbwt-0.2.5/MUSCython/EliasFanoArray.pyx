#!python
#cython: boundscheck=False
#cython: wraparound=False

import math
import numpy as np
cimport numpy as np
import time

cdef unsigned long samplingBits = 10
cdef unsigned long samplingSize = 2**samplingBits

cdef class EliasFanoArray(object):
    '''
    EliasFanoArray - http://vigna.di.unimi.it/ftp/papers/Broadword.pdf is where the broadword impl comes from
    This class is an implementation of an encoding I found online for storing monotonically increasing numbers.  In general,
    it splits all the numbers into upper and lower bits.  The lower bits are stored exactly as is.  The upper bits use a unary
    encoding based on the lower bits.  For example, if 10 bits are used for the lower bits, then the upper bin size is 2**10.  
    Then, the numbers are represented as 0s and 1s where a 0 indicates an increase in bin size and 1 indicates a number.
    Example:
    input values: [0, 3, 3, 8]
    max value = 8
    num values = 4
    lower bit size = 1
    upper bin size = 2
    lower bits = [0, 1, 1, 0]
    upper bits = 10110001
    '''
    def __cinit__(EliasFanoArray self, unsigned long maxValue, unsigned long numValues, logger=None):
        '''
        Constructor, I use __cinit__ because we instantiate a lot of these and it seems faster if everything
        is just basic values (like unsigned longs)
        @param maxValue - the maximum value we can store
        @param numValues - the number of values we will store
        @param logger - will log certain things if a logger is passed in
        '''
        self.previousValue = 0
        #self.valuesStored = []
        
        self.maxValue = maxValue
        self.maxStored = numValues
        self.numValues = 0
        
        if numValues == 0:
            self.lowerBitSize = 0
        else:
            self.lowerBitSize = max(0, math.floor(math.log(1.0*maxValue/numValues, 2)))
        
        self.upperBinSize = 2**self.lowerBitSize
        self.lowerBitsMask = (0xFFFFFFFFFFFFFFFF >> (64-self.lowerBitSize))
        
        cdef unsigned long lowerStorageSize = math.ceil(1.0*self.lowerBitSize*numValues/64.0)
        cdef unsigned long upperStorageSize = math.ceil(1.0*(numValues+math.ceil(1.0*maxValue/self.upperBinSize))/64.0)
        
        self.lowerBits = np.zeros(dtype='<u8', shape=(lowerStorageSize, ))
        self.lowerBits_view = self.lowerBits
        
        self.upperBits = np.zeros(dtype='<u8', shape=(upperStorageSize, ))
        self.upperBits_view = self.upperBits
        
        if logger:
            logger.info('Allocating '+str(8*(lowerStorageSize+upperStorageSize))+'B for EFA...')
        
        self.writeBins = 0
        self.writeUpperBits = 0
        self.writeLowerBits = 0
        
        self.nextSample = 0
        self.maxSampledIndex = 0
        cdef unsigned long numSamples = math.ceil(numValues/samplingSize)+1
        self.samples = np.zeros(dtype='<u8', shape=(numSamples, ))
        self.samples_view = self.samples
        
    cpdef addValue(EliasFanoArray self, unsigned long valueToAdd):
        '''
        This function will add the next value into the array 
        @param valueToAdd - the number to add, must be >= the previous added value
        '''
        #TODO: do we want to remove these checks in the final version?
        if self.numValues >= self.maxStored:
            raise Exception('EliasFanoArray row is full.')
        
        if valueToAdd > self.maxValue:
            raise Exception(str(valueToAdd)+' value to add exceeds maximum allowed value of '+str(self.maxValue))
        
        if valueToAdd < self.previousValue:
            raise Exception(str(valueToAdd)+' value is smaller than previous value of '+str(self.previousValue))
            
        cdef unsigned long lowerBits = valueToAdd & self.lowerBitsMask
        cdef unsigned long upperBin = valueToAdd >> self.lowerBitSize
        
        #first handle the upper bits, we need to skip enough 0s equal to the number of bins we advance, then set a bit
        #finally update the bin we just wrote to as well
        self.writeUpperBits += (upperBin - self.writeBins)
        setBit(self.upperBits_view, self.writeUpperBits)
        
        #check if we need to store a sampling bit location
        if self.numValues == self.nextSample:
            self.maxSampledIndex = self.nextSample/samplingSize
            self.samples_view[self.nextSample/samplingSize] = self.writeUpperBits
            self.nextSample += samplingSize
        
        self.writeUpperBits += 1
        self.writeBins = upperBin
        
        #now fill in some lower bits
        cdef unsigned long x
        for x in range(0, self.lowerBitSize):
            if (lowerBits & 0x1):
                setBit(self.lowerBits_view, self.writeLowerBits)
            lowerBits = lowerBits >> 1
            self.writeLowerBits += 1
        
        #self.valuesStored.append(valueToAdd)
        self.previousValue = valueToAdd
        self.numValues += 1
    
    cpdef unsigned long getNumValues(EliasFanoArray self):
        return self.numValues
    
    cpdef np.ndarray getLowerBits(EliasFanoArray self):
        return self.lowerBits
    
    cpdef np.ndarray getUpperBits(EliasFanoArray self):
        return self.upperBits
    
    cpdef unsigned long getValueAtIndex(EliasFanoArray self, unsigned long index):
        '''
        This function returns a number from the EFA as if it were a basic array
        @param index - the index of the value to return
        @return - unsigned long that is the value stored at that index
        '''
        #use the sampling to skip ahead in our array
        cdef unsigned long startingBit = self.samples_view[index >> samplingBits]
        cdef unsigned long numBins = startingBit >> 6
        cdef unsigned long numOnes = ((index >> samplingBits) << samplingBits)+1
        cdef unsigned long numBitsUsed = startingBit & 0x3F
        numOnes -= getNumOnes(self.upperBits_view[numBins] & ((<unsigned long>0xFFFFFFFFFFFFFFFF >> (63 - numBitsUsed))))
        
        cdef unsigned long nextOnes = getNumOnes(self.upperBits_view[numBins])
        
        #then skip ahead to the right 64 bit number with the ones we want
        while numOnes + nextOnes < index:
            numOnes += nextOnes
            numBins += 1
            nextOnes = getNumOnes(self.upperBits_view[numBins])
        
        #now go on a bit-by-bit basis
        cdef unsigned long currentBit = 64*numBins
        while numOnes <= index:
            if getBit(self.upperBits_view, currentBit):
                numOnes += 1
            currentBit += 1
        
        #our number is a combination of the one we just found and the lower bits
        cdef unsigned long ret = ((currentBit - numOnes) << self.lowerBitSize)
        
        currentBit = self.lowerBitSize*index
        cdef unsigned long x
        for x in range(0, self.lowerBitSize):
            ret += (<unsigned long>getBit(self.lowerBits_view, currentBit)) << x
            currentBit += 1
        
        return ret
    
    cpdef unsigned long countLessThanValue(EliasFanoArray self, unsigned long value):
        '''
        This should return the number of numbers in the EFA that are strictly less than the passed value
        @param value - all numbers in the count are strictly less than value
        @return - an integer representing how many values in the array are less
        '''
        if value > self.previousValue:
            return self.numValues
        
        cdef unsigned long l = 0
        cdef unsigned long h = self.maxSampledIndex
        cdef unsigned m
        
        #this is the number of zeroes we need to find
        cdef unsigned long numReqZeroes = value >> self.lowerBitSize
        cdef unsigned long reqLowerBits = value & self.lowerBitsMask
        
        cdef unsigned long numZeroes
        
        #first, we binary search for where to start
        while l != h:
            m = (l+h)/2
            
            #basically read as: numZeroes = numBits - numOnes
            numZeroes = self.samples_view[m] - (m << samplingBits)
            if numZeroes < numReqZeroes:
                l = m+1
            else:
                h = m
        
        #backtrack to before the value
        numZeroes = self.samples_view[l] - (l << samplingBits)
        while numZeroes >= numReqZeroes:
            if l > 0:
                l -= 1
                numZeroes = self.samples_view[l] - (l << samplingBits)
            else:
                if numReqZeroes < numZeroes:
                    return 0
                else:
                    break
        
        #now we basically count numZeroes as related to numOnes
        cdef unsigned long startingBit = self.samples_view[l]
        cdef unsigned long numBins = startingBit >> 6
        cdef unsigned long numOnes = (l << samplingBits)+1
        cdef unsigned long numBitsUsed = startingBit & 0x3F
        numOnes -= getNumOnes(self.upperBits_view[numBins] & ((<unsigned long>0xFFFFFFFFFFFFFFFF >> (63 - numBitsUsed))))
        numZeroes = (numBins << 6) - numOnes
        
        #this will store the number of zeroes and ones in the next 64 bit value
        cdef unsigned long nextOnes = getNumOnes(self.upperBits_view[numBins])
        cdef unsigned long nextZeroes = 64-nextOnes
        
        #loop through to find which bucket will cause us to pass where we want to be
        while numZeroes + nextZeroes < numReqZeroes:
            numOnes += nextOnes
            numZeroes += nextZeroes
            numBins += 1
            nextOnes = getNumOnes(self.upperBits_view[numBins])
            nextZeroes = 64 - nextOnes
        
        #go through one bit at a time now
        cdef unsigned long currentBit = 64*numBins
        while numZeroes < numReqZeroes:
            if getBit(self.upperBits_view, currentBit):
                numOnes += 1
            else:
                numZeroes += 1
            currentBit += 1
        
        #now check the numbers that can't be determined solely by the upper bits
        cdef unsigned long x, lCurrentBit, lValue
        while getBit(self.upperBits_view, currentBit):
            lCurrentBit = self.lowerBitSize*numOnes
            lValue = 0
            for x in range(0, self.lowerBitSize):
                lValue += (<unsigned long>getBit(self.lowerBits_view, lCurrentBit)) << x
                lCurrentBit += 1
            
            if lValue < reqLowerBits:
                numOnes += 1
                currentBit += 1
            else:
                break
        
        #return what we found
        return numOnes
            
cdef inline void setBit(np.uint64_t [:] bitArray, unsigned long index) nogil:
    #set a bit in an array
    bitArray[index >> 6] |= (<unsigned long>0x1 << (index & 0x3F))

cdef inline void clearBit(np.uint64_t [:] bitArray, unsigned long index) nogil:
    #clear a bit in an array
    bitArray[index >> 6] &= ~(<unsigned long>0x1 << (index & 0x3F))

cdef inline bint getBit(np.uint64_t [:] bitArray, unsigned long index) nogil:
    #get a bit from an array
    return (bitArray[index >> 6] >> (index & 0x3F)) & 0x1

cdef inline unsigned long getNumOnes(unsigned long value) nogil:
    '''
    from http://vigna.di.unimi.it/ftp/papers/Broadword.pdf
    TODO: remove the multiply?
    '''
    cdef unsigned long ret = value-((value & <unsigned long>0xAAAAAAAAAAAAAAAA) >> 1)
    ret = (ret & <unsigned long>0x3333333333333333) + ((ret >> 2) & <unsigned long>0x3333333333333333)
    ret = (ret + (ret >> 4)) & <unsigned long>0x0F0F0F0F0F0F0F0F
    return (ret * <unsigned long>0x0101010101010101) >> 56
