#!python
#cython: boundscheck=False
#cython: wraparound=False

import math
import numpy as np
cimport numpy as np
import sys
import time

cimport BasicBWT
from EliasFanoArray cimport EliasFanoArray as EFA

cdef unsigned long EFA_THRESHOLD = 20

cdef class NumericalBWT(BasicBWT.BasicBWT):
    '''
    This subclass of the BasicBWT is meant only for the linear merge implementation.  It can represent a bwt with any 
    number of symbols (aka, more than 6 symbols) and uses EFAs as forward index structures instead of the typical sampled 
    FM-index.  As such, queries to it are somewhat different in terms of implementation.
    '''
    #cdef unsigned long bitsPerSymbol
    #cdef unsigned long bitMask
    
    cpdef allocateMsbwt(NumericalBWT self, unsigned long vcLen, unsigned long numSymbols, logger=None):
        '''
        This functions loads a BWT file and prepares it to have values set in it
        @param vcLen - the size of the alphabet
        @param numSymbols - the number of symbols in the bwt
        @param logger - the logger to print output to (default: None)
        '''
        #first, reset our vcLen to the new value
        self.vcLen = vcLen
        
        #we need to pre-allocate the bwt space
        if self.vcLen <= 2:
            self.bitsPerSymbol = 1
        else:
            self.bitsPerSymbol = math.ceil(math.log(self.vcLen, 2))
        self.bitMask = (0xFFFFFFFFFFFFFFFF >> (64-self.bitsPerSymbol))
        cdef unsigned long bwtSize = math.ceil((self.bitsPerSymbol*numSymbols+1)/8.0)
        logger.info('Allocating '+str(bwtSize)+'B for BWT...')
        self.bwt = np.zeros(shape=(bwtSize, ), dtype='<u1')
        self.bwt_view = self.bwt
        
        #build totalCounts as we go since it's easy to do
        self.totalCounts = np.zeros(dtype='<u8', shape=(self.vcLen, ))
        self.totalCounts_view = self.totalCounts
        self.totalSize = numSymbols
        
    cpdef presetValueAtIndex(NumericalBWT self, unsigned long value, unsigned long index):
        '''
        This function will set a position in the BWT to a specific value.  It's really only meant to be called for 
        construction since it also increments the totalCounts.  As a result, each index can only be set once.  When 
        done setting everything, call finalizeAllocate(...) to finish it up.
        @param value - the value to set the index to 
        @param index - the position to set
        '''
        #set the value with our inline function
        self.setValueAtIndex(value, index)
        
        #update total counts
        self.totalCounts_view[value] += 1
        
    cpdef finalizeAllocate(NumericalBWT self, unsigned long trueVCLen, logger=None):
        '''
        Once all the values have been added to the bwt using presetValueAtIndex(...), call this function to construct 
        any necessary indices.
        @param trueVCLen - the actual vcLen as calculated somewhere else
        @param logger - pass in for debug purposes
        '''
        #first, change the vcLen now that we know it
        self.vcLen = trueVCLen
        if logger:
            logger.info('Finalizing BWT allocation..')
        
        #build auxiliary structures
        self.constructIndexing()
        self.constructForwardIndices(logger)
    
    cdef void constructForwardIndices(NumericalBWT self, logger):
        '''
        This constructs forward indices in place of the FM index using EFA.
        @param logger - the logger to use for output
        '''
        logger.info('Constructing forward indices...')
        self.forwardIndices = [None]*self.vcLen
        cdef unsigned long x
        for x in range(0, self.vcLen):
            if self.totalCounts_view[x] == 0:
                pass
            elif self.totalCounts_view[x] < EFA_THRESHOLD:
                self.forwardIndices[x] = []
            else:
                self.forwardIndices[x] = EFA(self.totalSize, self.totalCounts_view[x])
        
        logger.info('Filling indices...')
        cdef unsigned long sym
        for x in range(0, self.totalSize):
            sym = self.getValueAtIndex(x)
            if self.totalCounts_view[sym] < EFA_THRESHOLD:
                (<list>self.forwardIndices[sym]).append(x)
            else:
                (<EFA>self.forwardIndices[sym]).addValue(x)
    
    cpdef list getForwardIndices(NumericalBWT self):
        return self.forwardIndices
    
    cpdef np.ndarray[np.uint64_t, ndim=1, mode='c'] getFullFMAtIndex(NumericalBWT self, unsigned long index):
        '''
        This function creates a complete FM-index for a specific position in the BWT.  Example using the above example:
        BWT    Full FM-index
                 $ A C G T
        C        0 1 2 4 4
        $        0 1 3 4 4
        C        1 1 3 4 4
        A        1 1 4 4 4
                 1 2 4 4 4
        @return - the above information in the form of an array that already incorporates the offset value into the counts
        '''
        cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] ret = np.empty(dtype='<u8', shape=(self.vcLen, ))
        cdef np.uint64_t [:] ret_view = ret
        
        cdef unsigned long sym
        cdef unsigned long x
        for sym in range(0, self.vcLen):
            if self.forwardIndices[sym] == None:
                ret_view[sym] = self.startIndex_view[sym]
            elif self.totalCounts_view[sym] < EFA_THRESHOLD:
                ret_view[sym] = self.startIndex_view[sym]
                x = 0
                while x < self.totalCounts_view[sym] and (<list>self.forwardIndices[sym])[x] < index:
                    ret_view[sym] += 1
                    x += 1
            else:
                ret_view[sym] = self.startIndex_view[sym]+(<EFA>self.forwardIndices[sym]).countLessThanValue(index)
        
        return ret
    
    cdef void fillFmAtIndex(NumericalBWT self, np.uint64_t [:] fill_view, unsigned long index):
        '''
        Same as getFmAtIndex, but with a pass in array to fill in
        @param fill_view - the view of the fmIndex we are going to fill in
        @param index - the index to extract the fm-index for
        '''
        cdef unsigned long sym, x
        for sym in range(0, self.vcLen):
            if self.forwardIndices[sym] == None:
                fill_view[sym] = self.startIndex_view[sym]
            elif self.totalCounts_view[sym] < EFA_THRESHOLD:
                fill_view[sym] = self.startIndex_view[sym]
                x = 0
                while x < self.totalCounts_view[sym] and (<list>self.forwardIndices[sym])[x] < index:
                    fill_view[sym] += 1
                    x += 1
            else:
                fill_view[sym] = self.startIndex_view[sym]+(<EFA>self.forwardIndices[sym]).countLessThanValue(index)
        
    cpdef unsigned long getOccurrenceOfCharAtIndex(NumericalBWT self, unsigned long sym, unsigned long index):# nogil:
        '''
        This functions gets the FM-index value of a character at the specified position
        @param sym - the character to find the occurrence level
        @param index - the index we want to find the occurrence level at
        @return - the number of occurrences of char before the specified index
        '''
        cdef unsigned long ret, x
        cdef list fi
        if self.forwardIndices[sym] == None:
            return self.startIndex_view[sym]
        elif self.totalCounts_view[sym] < EFA_THRESHOLD:
            ret = self.startIndex_view[sym]
            x = 0
            fi = <list>self.forwardIndices[sym]
            while x < self.totalCounts_view[sym] and <unsigned long>(fi[x]) < index:
                #ret += 1
                x += 1
            return ret+x
        else:
            return self.startIndex_view[sym] + (<EFA>self.forwardIndices[sym]).countLessThanValue(index)
        
    cpdef unsigned long getCharAtIndex(NumericalBWT self, unsigned long index):
        '''
        Return the symbol at the given index
        @param index - the index to get the symbol from
        '''
        return self.getValueAtIndex(index)
    
    cdef inline void setValueAtIndex(NumericalBWT self, unsigned long value, unsigned long index):
        '''
        sets the value at the given index
        @param value - the value to set the index to
        @param index - the index we want to set
        '''
        cdef unsigned long startingBit = index*self.bitsPerSymbol
        cdef unsigned long x
        for x in range(0, self.bitsPerSymbol):
            #if value & 0x1:
            #    setBit(self.bwt_view, startingBit)
            self.bwt_view[startingBit >> 3] |= ((value & <unsigned long>0x1) << (startingBit & 0x7))
            value = value >> 1
            startingBit += 1
    
    cdef inline unsigned long getValueAtIndex(NumericalBWT self, unsigned long index):
        '''
        get the value at a given index
        @param index - the position to get
        '''
        return getBits(self.bwt_view, index*self.bitsPerSymbol, self.bitsPerSymbol, self.bitMask)
            
cdef inline void setBit(np.uint8_t [:] bitArray, unsigned long index) nogil:
    #set a bit in an array
    bitArray[index >> 3] |= (0x1 << (index & 0x7))

cdef inline unsigned long getBits(np.uint8_t [:] bitArray, unsigned long index, unsigned long numBits, unsigned long mask):
    #TODO: maybe convert this to 64-bits so we can do simple math?
    cdef unsigned long ret = 0
    cdef unsigned long x
    cdef unsigned long i = 0
    for x in range(index >> 3, ((index+numBits) >> 3)+1):
        ret += (<unsigned long>bitArray[x]) << i
        i += 8
    ret = (ret >> (index & 0x7)) & mask
    return ret
            