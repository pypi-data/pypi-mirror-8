#!python
#cython: boundscheck=False
#cython: wraparound=False

import math
import numpy as np
cimport numpy as np
import os
import time

import MultiStringBWTCython as MultiStringBWT
from BasicBWT cimport BasicBWT
from EliasFanoArray cimport EliasFanoArray2D

def bucketMerge(char * inputBwtDir1, char * inputBwtDir2, char * mergeDir, unsigned long numProcs, logger):
    '''
    This is another version of the merge algorithm that is entirely bucket based.
    @param inputBwtDir1 - the directory (string format) of the first bwt
    @param inputBwtDir2 - the directory (string format) of the second bwt
    @param mergeDir - the directory (string format) of the output bwt
    @param numProcs - the number of processes this is allowed to use
    @param logger - the logger for output
    '''
    logger.info('Input 1: '+inputBwtDir1)
    logger.info('Input 2: '+inputBwtDir2)
    logger.info('Output : '+mergeDir)
    logger.info('Multiprocessing is not enabled at this time.')
    
    cdef unsigned long vcLen = 6
    
    cdef BasicBWT bwt1 = MultiStringBWT.loadBWT(inputBwtDir1, useMemmap=False, logger=logger)
    cdef BasicBWT bwt2 = MultiStringBWT.loadBWT(inputBwtDir2, useMemmap=False, logger=logger)
    
    cdef unsigned long ts1 = bwt1.getTotalSize()
    cdef unsigned long ts2 = bwt2.getTotalSize()
    
    cdef unsigned long binBits1 = bwt1.getBinBits()
    cdef unsigned long binBits2 = bwt2.getBinBits()
    cdef unsigned long binSize1 = 2**binBits1
    cdef unsigned long binSize2 = 2**binBits2
    
    cdef unsigned long efaSize1 = 2
    cdef unsigned long efaSize2 = 2
    cdef EliasFanoArray2D readEfa1 = EliasFanoArray2D(ts1, efaSize1, 1)
    readEfa1.addValue(0, 0)
    readEfa1.addValue(0, ts1)
    cdef EliasFanoArray2D readEfa2 = EliasFanoArray2D(ts2, efaSize2, 1)
    readEfa2.addValue(0, 0)
    readEfa2.addValue(0, ts2)
    
    cdef EliasFanoArray2D prevEfa1 = EliasFanoArray2D(ts1, efaSize1, 1)
    cdef EliasFanoArray2D prevEfa2 = EliasFanoArray2D(ts2, efaSize2, 1)
    
    cdef unsigned long interleaveShape = math.ceil(1.0*(ts1+ts2)/8.0)
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] interleave = np.zeros(dtype='<u1', shape=(interleaveShape, ))
    cdef np.uint8_t [:] interleave_view = interleave
    
    cdef unsigned long i = 0
    cdef unsigned long x, y
    cdef unsigned long maxSize
    
    cdef EliasFanoArray2D writeEfa1
    cdef EliasFanoArray2D writeEfa2
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] numUses
    cdef np.uint64_t [:] numUses_view
    
    cdef bint changesMade
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] sfi1, sfi2, efi1, efi2
    sfi1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    sfi2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    efi1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    efi2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    
    cdef np.uint64_t [:] sfi1_view, sfi2_view, efi1_view, efi2_view
    sfi1_view = sfi1
    sfi2_view = sfi2
    efi1_view = efi1
    efi2_view = efi2
    
    cdef unsigned long endIndex0
    cdef unsigned long endIndex1
    
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] efiBin1 = np.zeros(dtype='<u1', shape=(2**binBits1, ))
    cdef np.uint8_t [:] efiBin1_view = efiBin1
    
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] efiBin2 = np.zeros(dtype='<u1', shape=(2**binBits2, ))
    cdef np.uint8_t [:] efiBin2_view = efiBin2
    
    cdef unsigned long tnu
    
    cdef unsigned long rangeStart1, rangeEnd1
    cdef unsigned long rangeStart2, rangeEnd2
    
    while not (prevEfa1.getNumValues() == readEfa1.getNumValues() and
               prevEfa2.getNumValues() == readEfa2.getNumValues() and
               np.array_equal(prevEfa1.getLowerBits(), readEfa1.getLowerBits()) and
               np.array_equal(prevEfa1.getUpperBits(), readEfa1.getUpperBits()) and
               np.array_equal(prevEfa2.getLowerBits(), readEfa2.getLowerBits()) and
               np.array_equal(prevEfa2.getUpperBits(), readEfa2.getUpperBits())):
        #logger.info('Handling '+str(i)+'-mers with '+str(currRanges.shape[0])+' entries...')
        logger.info('Handling '+str(i)+'-mers with '+str(readEfa1.getNumValues()/2)+' entries...')
        i += 1
        
        prevEfa1 = readEfa1
        prevEfa2 = readEfa2
        readEfa1.resetReader(0)
        readEfa2.resetReader(0)
        maxSize = readEfa1.getNumValues()
        
        writeEfa1 = EliasFanoArray2D(ts1, maxSize, vcLen)
        writeEfa2 = EliasFanoArray2D(ts2, maxSize, vcLen)
        
        numUses = np.zeros(dtype='<u8', shape=(vcLen, ))
        numUses_view = numUses
        
        #initialize all indices to values corresponding to bin 0, index 0 
        bwt1.fillFmAtIndex(sfi1_view, 0)
        bwt1.fillFmAtIndex(efi1_view, 0)
        bwt2.fillFmAtIndex(sfi2_view, 0)
        bwt2.fillFmAtIndex(efi2_view, 0)
        endIndex1 = 0
        endIndex2 = 0
        bwt1.fillBin(efiBin1_view, 0)
        bwt2.fillBin(efiBin2_view, 0)
        
        for x in range(0, readEfa1.getNumValues()/2):
            rangeStart1 = readEfa1.decodeValue()
            rangeEnd1 = readEfa1.decodeValue()
            rangeStart2 = readEfa2.decodeValue()
            rangeEnd2 = readEfa2.decodeValue()
            
            if rangeStart1 == rangeEnd1:
                changesMade = False
                #all ones range
                for y in range(rangeStart1+rangeStart2, rangeStart1+rangeEnd2):
                    if getBit(interleave_view, y):
                        pass
                    else:
                        setBit(interleave_view, y)
                        changesMade = True
                
                if changesMade:
                    #propagate the range
                    for y in range(0, vcLen):
                        sfi1_view[y] = efi1_view[y]
                    updateFmIndex(sfi1_view, bwt1, efiBin1_view, binBits1, endIndex1, rangeStart1)
                    endIndex1 = rangeStart1
                    
                    for y in range(0, vcLen):
                        efi1_view[y] = sfi1_view[y]
                    updateFmIndex(efi1_view, bwt1, efiBin1_view, binBits1, endIndex1, rangeEnd1)
                    endIndex1 = rangeEnd1
                    
                    for y in range(0, vcLen):
                        sfi2_view[y] = efi2_view[y]
                    updateFmIndex(sfi2_view, bwt2, efiBin2_view, binBits2, endIndex2, rangeStart2)
                    endIndex2 = rangeStart2
                    
                    for y in range(0, vcLen):
                        efi2_view[y] = sfi2_view[y]
                    updateFmIndex(efi2_view, bwt2, efiBin2_view, binBits2, endIndex2, rangeEnd2)
                    endIndex2 = rangeEnd2
                    
                    for y in range(0, vcLen):
                        if sfi2_view[y] != efi2_view[y]:
                            writeEfa1.addValue(y, sfi1_view[y])
                            writeEfa1.addValue(y, sfi1_view[y])
                            writeEfa2.addValue(y, sfi2_view[y])
                            writeEfa2.addValue(y, efi2_view[y])
                            numUses_view[y] += 1
            elif rangeStart2 == rangeEnd2:    
                #do nothing here
                pass
            else:
                #both zeros and ones in the range
                for y in range(0, vcLen):
                    sfi1_view[y] = efi1_view[y]
                updateFmIndex(sfi1_view, bwt1, efiBin1_view, binBits1, endIndex1, rangeStart1)
                endIndex1 = rangeStart1
                
                for y in range(0, vcLen):
                    efi1_view[y] = sfi1_view[y]
                updateFmIndex(efi1_view, bwt1, efiBin1_view, binBits1, endIndex1, rangeEnd1)
                endIndex1 = rangeEnd1
                
                for y in range(0, vcLen):
                    sfi2_view[y] = efi2_view[y]
                updateFmIndex(sfi2_view, bwt2, efiBin2_view, binBits2, endIndex2, rangeStart2)
                endIndex2 = rangeStart2
                
                for y in range(0, vcLen):
                    efi2_view[y] = sfi2_view[y]
                updateFmIndex(efi2_view, bwt2, efiBin2_view, binBits2, endIndex2, rangeEnd2)
                endIndex2 = rangeEnd2
                
                for y in range(0, vcLen):
                    if sfi1_view[y] != efi1_view[y] or sfi2_view[y] != efi2_view[y]:
                        writeEfa1.addValue(y, sfi1_view[y])
                        writeEfa1.addValue(y, efi1_view[y])
                        writeEfa2.addValue(y, sfi2_view[y])
                        writeEfa2.addValue(y, efi2_view[y])
                        numUses_view[y] += 1
        
        readEfa1 = writeEfa1
        readEfa2 = writeEfa2
        
    for x in range(0, np.sum(numUses)):
        rangeStart1 = readEfa1.decodeValue()
        rangeEnd1 = readEfa1.decodeValue()
        rangeStart2 = readEfa2.decodeValue()
        rangeEnd2 = readEfa2.decodeValue()
        for y in range(rangeEnd1+rangeStart2, rangeEnd1+rangeEnd2):
            setBit(interleave_view, y)
    
    #need to fill in the actually bwt
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] resultBwt = np.lib.format.open_memmap(mergeDir+'/msbwt.npy', 'w+', '<u1', (ts1+ts2, ))
    cdef np.uint8_t [:] resultBwt_view = resultBwt
    
    cdef unsigned long binUse1 = 0
    cdef unsigned long binUse2 = 0
    cdef unsigned long binID1 = 0
    cdef unsigned long binID2 = 0
    bwt1.fillBin(efiBin1_view, 0)
    bwt2.fillBin(efiBin2_view, 0)
    
    logger.info('Writing merged result...')
    for x in range(0, ts1+ts2):
        if getBit(interleave_view, x):
            resultBwt_view[x] = efiBin2_view[binUse2]
            binUse2 += 1
            if binUse2 == binSize2:
                binID2 += 1
                bwt2.fillBin(efiBin2_view, binID2)
                binUse2 = 0
        else:
            resultBwt_view[x] = efiBin1_view[binUse1]
            binUse1 += 1
            if binUse1 == binSize1:
                binID1 += 1
                bwt1.fillBin(efiBin1_view, binID1)
                binUse1 = 0

cdef inline void updateFmIndex(np.uint64_t [:] fmIndex_view, BasicBWT bwt, np.uint8_t [:] currentBin, unsigned long binBits,
                               unsigned long previousIndex, unsigned long updateIndex):
    '''
    '''
    cdef unsigned long binSize = 2**binBits
    cdef unsigned long binIndex = updateIndex >> binBits
    cdef unsigned long binStart = binIndex << binBits
    cdef unsigned long x
    
    #check if we're already in the right bin
    if binIndex == (previousIndex >> binBits):
        #easy mode, just advance along the bin some
        for x in range(previousIndex - binStart, updateIndex - binStart):
            fmIndex_view[currentBin[x]] += 1
    else:
        #hard mode, fill in the FM-index
        bwt.fillFmAtIndex(fmIndex_view, binStart)
        bwt.fillBin(currentBin, binIndex)
        for x in range(0, updateIndex - binStart):
            fmIndex_view[currentBin[x]] += 1

cdef inline void setBit(np.uint8_t [:] bitArray, unsigned long index) nogil:
    #set a bit in an array
    bitArray[index >> 3] |= (0x1 << (index & 0x7))

cdef inline void clearBit(np.uint8_t [:] bitArray, unsigned long index) nogil:
    #clear a bit in an array
    bitArray[index >> 3] &= ~(0x1 << (index & 0x7))

cdef inline bint getBit(np.uint8_t [:] bitArray, unsigned long index) nogil:
    #get a bit from an array
    return (bitArray[index >> 3] >> (index & 0x7)) & 0x1
        