#!python
#cython: boundscheck=False
#cython: wraparound=False

import math
import numpy as np
cimport numpy as np
import time

cdef class EliasFanoArray2D(object):
    '''
    
    '''
    def __init__(EliasFanoArray2D self, unsigned long maxValue, unsigned long numValuesPerRow, unsigned long numRows):
        '''
        Constructor
        @param maxValue - the maximum value we can store
        @param numValues - the number of values we will store
        '''
        #self.previousValue = 0
        #self.valuesStored = []
        
        self.maxValue = maxValue
        self.maxStoredPerRow = numValuesPerRow
        self.numValues = np.zeros(dtype='<u8', shape=(numRows, ))
        self.numValues_view = self.numValues
        
        if numValuesPerRow == 0:
            self.lowerBitSize = 0
        else:
            self.lowerBitSize = max(0, math.floor(math.log(1.0*maxValue/numValuesPerRow, 2)))
        #self.lowerBitSize += 0
        
        self.upperBinSize = 2**self.lowerBitSize
        self.lowerBitsMask = (0xFFFFFFFFFFFFFFFF >> (64-self.lowerBitSize))
        
        cdef unsigned long lowerStorageSize = math.ceil(1.0*self.lowerBitSize*numValuesPerRow/8.0)
        
        #TODO: 2 was too small, 3 is likely overkill, there's some value inbetween for it, a function of numvalues and numbuckets for sure
        #TODO: maybe using math.ceil earlier and 2.0 will work
        #cdef unsigned long upperStorageSize = math.ceil(3.0*numValuesPerRow/8.0)
        cdef unsigned long upperStorageSize = math.ceil(1.0*(numValuesPerRow+math.ceil(1.0*maxValue/self.upperBinSize))/8.0)
        
        
        #print 'Allocating '+str(lowerStorageSize+upperStorageSize)+' bytes.'
        
        self.lowerBits = np.zeros(dtype='<u1', shape=(numRows, lowerStorageSize))
        self.lowerBits_view = self.lowerBits
        
        self.upperBits = np.zeros(dtype='<u1', shape=(numRows, upperStorageSize))
        self.upperBits_view = self.upperBits
        
        #self.writeBin = 0
        #self.writeUpperBit = 0
        #self.writeLowerBit = 0
        self.writeBins = np.zeros(dtype='<u8', shape=(numRows, ))
        self.writeUpperBits = np.zeros(dtype='<u8', shape=(numRows, ))
        self.writeLowerBits = np.zeros(dtype='<u8', shape=(numRows, ))
        self.writeBins_view = self.writeBins
        self.writeUpperBits_view = self.writeUpperBits
        self.writeLowerBits_view = self.writeLowerBits
        
        self.readRow = 0
        self.readBin = 0
        self.readUpperBit = 0
        self.readLowerBit = 0
        self.numRead = 0
        self.firstOnes = np.zeros(dtype='<u8', shape=(numRows, ))
        self.firstOnes_view = self.firstOnes
        self.firstSet = np.zeros(dtype='<u1', shape=(numRows, ))
        self.firstSet_view = self.firstSet
        
        #print self.lowerBitSize, self.upperBinSize
        #print lowerStorageSize, upperStorageSize
    
    cpdef addValue(EliasFanoArray2D self, unsigned long row, unsigned long valueToAdd):
        #if self.numValues_view[row] >= self.maxStoredPerRow:
        #    raise Exception('EliasFanoArray row is full.')
        
        if valueToAdd > self.maxValue:
            raise Exception(str(valueToAdd)+' value to add exceeds maximum allowed value of '+str(self.maxValue))
        
        if valueToAdd < self.previousValue:
            raise Exception(str(valueToAdd)+' value is smaller than previous value of '+str(self.previousValue))
        
        self.numValues_view[row] += 1
        
        cdef unsigned long lowerBits = valueToAdd & self.lowerBitsMask
        cdef unsigned long upperBin = valueToAdd >> self.lowerBitSize
        
        if self.firstSet_view[row] == 0:
            self.firstOnes_view[row] = upperBin
            self.firstSet_view[row] = 1
        
        #print valueToAdd, lowerBits, upperBin
        
        #first handle the upper bits, we need to skip enough 0s equal to the number of bins we advance, then set a bit
        #finally update the bin we just wrote to as well
        self.writeUpperBits_view[row] += (upperBin - self.writeBins_view[row])
        setBit(self.upperBits_view, row, self.writeUpperBits_view[row])
        self.writeUpperBits_view[row] += 1
        self.writeBins_view[row] = upperBin
        
        #now fill in some lower bits
        cdef unsigned long x
        for x in range(0, self.lowerBitSize):
            if (lowerBits & 0x1):
                setBit(self.lowerBits_view, row, self.writeLowerBits_view[row])
            lowerBits = lowerBits >> 1
            self.writeLowerBits_view[row] += 1
        
        #print self.lowerBits, self.upperBits
        #self.valuesStored.append(valueToAdd)
        self.previousValue = valueToAdd
    
    cpdef unsigned long getNumValues(EliasFanoArray2D self):
        return np.sum(self.numValues)
    
    cpdef np.ndarray getLowerBits(EliasFanoArray2D self):
        return self.lowerBits
    
    cpdef np.ndarray getUpperBits(EliasFanoArray2D self):
        return self.upperBits
    
    cpdef resetReader(EliasFanoArray2D self, unsigned long row):
        '''
        This function will reset the reader back to the first value
        '''
        self.readRow = row
        #self.readBin = 0
        self.readBin = self.firstOnes_view[row]
        #self.readUpperBit = 0
        self.readUpperBit = self.firstOnes_view[row]
        self.readLowerBit = 0
        self.numRead = 0
    
    cpdef unsigned long decodeValue(EliasFanoArray2D self):
        '''
        This functions returns one value, it returns them in the order they are first by row, then by value
        @return - a single unsigned integer value
        '''
        
        #print 'EFA data', self.lowerBitSize, self.upperBinSize, self.readRow, self.numRead, self.numValues_view[self.readRow]
        #print 'EFA cont', self.upperBits, self.readUpperBit
        #print 'EFA vals', self.valuesStored
        
        while self.numRead >= self.numValues_view[self.readRow]:
            self.readRow += 1
            self.resetReader(self.readRow)
            
            if self.readRow >= self.numValues.shape[0]:
                raise Exception('Out of value to decode.')
        
        #first figure out the upper bin
        while getBit(self.upperBits_view, self.readRow, self.readUpperBit) == 0:
            #self.readBin += 1
            self.readUpperBit += 1
            if self.readUpperBit >= 8*self.upperBits.shape[1]:
                raise Exception('bad')
        self.readUpperBit += 1
        self.numRead += 1
        
        #print self.readBin
        #cdef unsigned long ret = (self.readBin << self.lowerBitSize)
        cdef unsigned long ret = ((self.readUpperBit-self.numRead) << self.lowerBitSize)
        
        #lower figure out the lower bits
        #'''
        cdef unsigned long x
        for x in range(0, self.lowerBitSize):
            ret += (<unsigned long>getBit(self.lowerBits_view, self.readRow, self.readLowerBit)) << x
            self.readLowerBit += 1
        '''
        ret += getBits(self.lowerBits_view, self.readRow, self.readLowerBit, self.lowerBitSize, self.lowerBitsMask)
        self.readLowerBit += self.lowerBitSize
        '''
        
        if ret > self.maxValue:
            raise Exception('bad')
        
        return ret

cdef inline void setBit(np.uint8_t [:, :] bitArray, unsigned long row, unsigned long index) nogil:
    #set a bit in an array
    bitArray[row, index >> 3] |= (0x1 << (index & 0x7))

cdef inline void clearBit(np.uint8_t [:, :] bitArray, unsigned long row, unsigned long index) nogil:
    #clear a bit in an array
    bitArray[row, index >> 3] &= ~(0x1 << (index & 0x7))

cdef inline bint getBit(np.uint8_t [:, :] bitArray, unsigned long row, unsigned long index) nogil:
    #get a bit from an array
    return (bitArray[row, index >> 3] >> (index & 0x7)) & 0x1

cdef inline unsigned long getBits(np.uint8_t [:, :] bitArray, unsigned long row, unsigned long index, unsigned long numBits, unsigned long mask) nogil:
    #cdef unsigned long mask = (0xFFFFFFFFFFFFFFFF >> (0x40-numBits))
    cdef unsigned long ret = 0
    cdef unsigned long x
    cdef unsigned long i = 0
    for x in range(index >> 3, ((index+numBits) >> 3)+1):
        ret += (<unsigned long>bitArray[row, x]) << i
        i += 8
    ret = (ret >> (index & 0x7)) & mask
    return ret