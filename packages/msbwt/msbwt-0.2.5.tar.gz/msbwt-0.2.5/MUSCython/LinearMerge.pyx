#!python
#cython: boundscheck=False
#cython: wraparound=False

from collections import deque
import math
import os
import time

from BasicBWT cimport BasicBWT
from EliasFanoArray cimport EliasFanoArray as EFA
from NumericalBWT cimport NumericalBWT

import numpy as np
cimport numpy as np

def linearMerge(BasicBWT bwt1, BasicBWT bwt2, char * outputMergeDir, logger):
    '''
    This is the implementation of the linear merge algorithm that takes two bwts and reduces them to shorter bwts with 
    larger alphabets
    @param bwt1 - the first bwt
    @param bwt2 - the second bwt
    @param outputMergeDir - the directory to write the output to
    @param logger - the logger we use for output
    '''
    cdef unsigned long startingVCLen = 6
    cdef unsigned long currVCLen = startingVCLen
    
    cdef list bwt1List = [bwt1]
    cdef list bwt2List = [bwt2]
    cdef list vcLens = [startingVCLen]
    
    logger.info('Input BWT sizes:\t'+str(bwt1.getTotalSize())+'\t'+str(bwt2.getTotalSize()))
    
    #do the first pass outside the loop
    logger.info('Reducing input BWTs...')
    
    cdef BasicBWT b1, b2
    (b1, b2, currVCLen) = reduceBWTs(bwt1, bwt2, currVCLen, logger)
    vcLens.append(currVCLen)
    
    logger.info('symbolShare()')
    cdef bint sharedKmers = symbolShare(b1, b2, currVCLen)
    bwt1List.append(b1)
    bwt2List.append(b2)
    
    #first, we need to iteratively reduce the BWT space
    while (b1.getTotalSize() > 0 and
           b2.getTotalSize() > 0 and
           sharedKmers):
        #with each loop, reduce the BWTs
        logger.info('Reducing level '+str(len(bwt1List)-1)+' BWTs...')
        (b1, b2, currVCLen) = reduceBWTs(b1, b2, currVCLen, logger)
        vcLens.append(currVCLen)
        
        #check if they still share symbols, if so we will loop again
        logger.info('symbolShare()')
        sharedKmers = symbolShare(b1, b2, currVCLen)
        bwt1List.append(b1)
        bwt2List.append(b2)
        
    #step one is to extract the last BWT interleave
    cdef unsigned long currentDepth = len(bwt1List)-1
    
    #build a bit vector that we're going to use as the interleave
    cdef unsigned long interleaveSize = math.ceil((b1.getTotalSize()+b2.getTotalSize())/8.0)
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] nextInterleave = np.zeros(dtype='<u1', shape=(interleaveSize, ))
    cdef np.uint8_t [:] nextInterleave_view = nextInterleave
    cdef unsigned long nextInterleaveLength = b1.getTotalSize()+b2.getTotalSize()
    
    #fill in the interleave with the high level BWT interleave
    cdef unsigned long offset = 0
    cdef unsigned long x, y, x2
    for x in range(0, currVCLen):
        offset += b1.getSymbolCount(x)
        for y in range(offset, offset+b2.getSymbolCount(x)):
            #nextInterleave[y] = 1
            setBit(nextInterleave_view, y)
        
        offset += b2.getSymbolCount(x)
    
    #TODO: make a better log output?
    print 'nI', nextInterleave
    
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] currInterleave
    cdef np.uint8_t [:] currInterleave_view
    cdef unsigned long currInterleaveLength
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] LValues
    cdef np.uint64_t [:] LValues_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] SValues
    cdef np.uint64_t [:] SValues_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] interleaveIndices
    cdef np.uint64_t [:] interleaveIndices_view
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] bwtIndices1
    cdef np.uint64_t [:] bwtIndices1_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] bwtIndices2
    cdef np.uint64_t [:] bwtIndices2_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] bwtLIndices1
    cdef np.uint64_t [:] bwtLIndices1_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] bwtLIndices2
    cdef np.uint64_t [:] bwtLIndices2_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] bwtHIndices1
    cdef np.uint64_t [:] bwtHIndices1_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] bwtHIndices2
    cdef np.uint64_t [:] bwtHIndices2_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] endIndices1
    cdef np.uint64_t [:] endIndices1_view
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] endIndices2
    cdef np.uint64_t [:] endIndices2_view
    
    cdef unsigned long offset1, offset2
    cdef unsigned long currIndex, sym
    cdef unsigned long LIndex1, LIndex2
    cdef unsigned long SIndex1, SIndex2
    cdef unsigned long sIndex1, sIndex2
    cdef bint sStarID
    cdef bint sID
    
    #need to loop through each of the pairs of reduced BWTs and expand them back out
    while currentDepth > 0:
        currentDepth -= 1
        logger.info('Expanding level '+str(currentDepth)+' BWTs...')
        
        #get the BWTs for this level and the vcLen
        b1 = bwt1List[currentDepth]
        b2 = bwt2List[currentDepth]
        currVCLen = vcLens[currentDepth]
        
        #move the next interleave into the current
        currInterleave = nextInterleave
        currInterleave_view = currInterleave
        currInterleaveLength = nextInterleaveLength
        
        #preallocate the interleave to fill in
        interleaveSize = math.ceil((b1.getTotalSize()+b2.getTotalSize())/8.0)
        nextInterleaveLength = b1.getTotalSize()+b2.getTotalSize()
        nextInterleave = np.zeros(dtype='<u1', shape=(interleaveSize,))
        nextInterleave_view = nextInterleave
        
        #preallocate L and S value
        LValues = np.zeros(dtype='<u8', shape=(currVCLen, ))
        LValues_view = LValues
        SValues = np.zeros(dtype='<u8', shape=(currVCLen, ))
        SValues_view = SValues
        interleaveIndices = np.zeros(dtype='<u8', shape=(currVCLen, ))
        interleaveIndices_view = interleaveIndices
        
        #preallocate these indices too
        bwtIndices1 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        bwtIndices1_view = bwtIndices1
        bwtIndices2 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        bwtIndices2_view = bwtIndices2
        bwtLIndices1 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        bwtLIndices1_view = bwtLIndices1
        bwtLIndices2 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        bwtLIndices2_view = bwtLIndices2
        bwtHIndices1 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        bwtHIndices1_view = bwtHIndices1
        bwtHIndices2 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        bwtHIndices2_view = bwtHIndices2
        endIndices1 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        endIndices1_view = endIndices1
        endIndices2 = np.zeros(dtype='<u8', shape=(currVCLen, ))
        endIndices2_view = endIndices2
        
        #first set all write offsets
        offset1 = 0
        offset2 = 0
        for x in range(0, currVCLen):
            interleaveIndices_view[x] = offset1+offset2
            bwtIndices1_view[x] = offset1
            bwtIndices2_view[x] = offset2
            offset1 += b1.getSymbolCount(x)
            offset2 += b2.getSymbolCount(x)
            endIndices1_view[x] = offset1
            endIndices2_view[x] = offset2
            
            SValues_view[x] = offset1+offset2
            
            bwtLIndices1_view[x], bwtHIndices1_view[x] = findSingleSymbolBounds(b1, x)
            bwtLIndices2_view[x], bwtHIndices2_view[x] = findSingleSymbolBounds(b2, x)
        
        #this is going forward and it covers both L values and S* values
        currIndex = 0
        for x in range(0, currVCLen):
            y = 0
            
            #first we treat the found L values
            lIndex1 = bwtIndices1_view[x]
            lIndex2 = bwtIndices2_view[x]
            while y < LValues_view[x]:
                if getBit(nextInterleave_view, interleaveIndices_view[x]+y):
                    sym = b2.getCharAtIndex(lIndex2)
                    lIndex2 += 1
                    if sym >= x:
                        setBit(nextInterleave, interleaveIndices_view[sym]+LValues_view[sym])
                else:
                    sym = b1.getCharAtIndex(lIndex1)
                    lIndex1 += 1
                
                if sym >= x:
                    LValues_view[sym] += 1
                y += 1
            
            #second we treat the S* symbols for this range
            sIndex1 = bwtHIndices1_view[x]
            sIndex2 = bwtHIndices2_view[x]
            
            #iterate only so far as we're in this symbol
            while ((sIndex1 < endIndices1_view[x] or
                    sIndex2 < endIndices2_view[x]) and
                   currIndex < currInterleaveLength):
                sStarID = getBit(currInterleave_view, currIndex)
                if not sStarID:
                    if sIndex1 >= endIndices1_view[x]:
                        break
                    while sIndex1 < endIndices1_view[x]:
                        sym = b1.getCharAtIndex(sIndex1)
                        sIndex1 += 1
                        if sym > x:
                            #this is an S*
                            currIndex += 1
                            LValues_view[sym] += 1
                            break
                else:
                    if sIndex2 >= endIndices2_view[x]:
                        break
                    while sIndex2 < endIndices2_view[x]:
                        sym = b2.getCharAtIndex(sIndex2)
                        sIndex2 += 1
                        if sym > x:
                            #this is an S*
                            #nextInterleave[interleaveIndices[sym]+LValues[sym]] = 1
                            setBit(nextInterleave_view, interleaveIndices_view[sym]+LValues_view[sym])
                            currIndex += 1
                            LValues_view[sym] += 1
                            break
        
        #this covers all 'U' values, aka uniform strings of the same symbol forever (due to cycling)
        for x in range(0, currVCLen):
            for y in range(bwtHIndices1_view[x]+bwtLIndices2_view[x], bwtHIndices1_view[x]+bwtHIndices2_view[x]):
                setBit(nextInterleave_view, y)
        
        #finally, this covers all (non-S*) S values, note we do these in reverse order
        for x2 in range(currVCLen, 0, -1):
            #hack for when we go to cython
            x = x2-1
            
            #get the s indices
            sIndex1 = endIndices1_view[x]-1
            sIndex2 = endIndices2_view[x]-1
            
            for y in range(endIndices1_view[x]+endIndices2_view[x]-1, bwtIndices1_view[x]+bwtIndices2_view[x]-1, -1):
                sID = getBit(nextInterleave_view, y)
                if sID:
                    sym = b2.getCharAtIndex(sIndex2)
                    if sym <= x:
                        #we found a normal S
                        SValues_view[sym] -= 1
                        setBit(nextInterleave_view, SValues_view[sym])
                    sIndex2 -= 1
                else:
                    sym = b1.getCharAtIndex(sIndex1)
                    if sym <= x:
                        #we found a normal S again
                        SValues_view[sym] -= 1
                        #no need to set to zero, it already is
                    sIndex1 -= 1
        
        #TODO: make this a logger statement or remove
        print nextInterleave
    
    #finally, use the interleave to build the result and store it in an output directory
    interleaveBwts(bwt1, bwt2, nextInterleave_view, outputMergeDir)

cpdef tuple reduceBWTs(BasicBWT bwt1, BasicBWT bwt2, unsigned long vcLen, logger):
    '''
    This function takes two generic BWTs and reduces them into smaller BWTs by representing the sequences differently,
    this is so they can be merged, so they must use a common alphabet after being reduced (i. e. not all symbols need to 
    be present in both, but they have to be in at least one of them)
    @param bwt1 - the first bwt to reduce
    @param bwt2 - the second bwt to reduce
    @param vcLen - the length of the alphabet of the inputs
    @param logger - used for output
    '''
    logger.info('Input alphabet size:\t'+str(vcLen))
    logger.info('Generating forward indices...')
    
    #first, build forward indices for each BWT
    cdef list forwardIndices1 
    cdef list forwardIndices2
    cdef unsigned long x, y, z
    cdef unsigned long sym
    
    #check if the forward indices are already in the BWT because it's a NumericalBWT
    cdef bint isNumerical1 = isinstance(bwt1, NumericalBWT)
    cdef bint isNumerical2 = isinstance(bwt2, NumericalBWT)
    
    if isNumerical1:
        #just retrieve it
        forwardIndices1 = bwt1.getForwardIndices()
    else:
        #need to build forward indices for each symbol
        forwardIndices1 = [None]*vcLen
        
        #allocate an EFA if we have at least one of the symbol
        for x in range(0, vcLen):
            if bwt1.getSymbolCount(x) > 0:
                forwardIndices1[x] = EFA(bwt1.getTotalSize(), bwt1.getSymbolCount(x))
        
        #fill in the values
        for x in range(0, bwt1.getTotalSize()):
            sym = bwt1.getCharAtIndex(x)
            (<EFA>forwardIndices1[sym]).addValue(x)
    
    if isNumerical2:
        #just retrieve it
        forwardIndices2 = bwt2.getForwardIndices()
    else:
        #need to build forward indices for each symbol
        forwardIndices2 = [None]*vcLen
        
        #allocate an EFA if we have at least one of the symbol
        for x in range(0, vcLen):
            if bwt2.getSymbolCount(x) > 0:
                forwardIndices2[x] = EFA(bwt2.getTotalSize(), bwt2.getSymbolCount(x))
        
        #fill in the values
        for x in range(0, bwt2.getTotalSize()):
            sym = bwt2.getCharAtIndex(x)
            (<EFA>forwardIndices2[sym]).addValue(x)
    
    logger.info('Counting S* values...')
    
    cdef unsigned long tsc1 = 0
    cdef unsigned long tsc2 = 0
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] startRanges1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] hRanges1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] endRanges1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] sCounts1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.uint64_t [:] startRanges1_view = startRanges1
    cdef np.uint64_t [:] hRanges1_view = hRanges1
    cdef np.uint64_t [:] endRanges1_view = endRanges1
    cdef np.uint64_t [:] sCounts1_view = sCounts1
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] startRanges2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] hRanges2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] endRanges2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] sCounts2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.uint64_t [:] startRanges2_view = startRanges2
    cdef np.uint64_t [:] hRanges2_view = hRanges2
    cdef np.uint64_t [:] endRanges2_view = endRanges2
    cdef np.uint64_t [:] sCounts2_view = sCounts2
    
    cdef unsigned long prevH1, prevH2
    cdef unsigned long h1, h2
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmIndexSpace1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.uint64_t [:] fmIndexSpace1_view = fmIndexSpace1
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmIndexSpace2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.uint64_t [:] fmIndexSpace2_view = fmIndexSpace2
    
    cdef unsigned long tempCount
    
    #second, identify S ranges and count the S*'s within
    for x in range(0, vcLen):
        #print 's* loop', x, vcLen
        
        #set the starting ranges
        startRanges1_view[x] = tsc1
        startRanges2_view[x] = tsc2
        
        #do this at the start
        tsc1 += bwt1.getSymbolCount(x)
        tsc2 += bwt2.getSymbolCount(x)
        
        #the end is at the total count so far
        endRanges1_view[x] = tsc1
        endRanges2_view[x] = tsc2
        
        #start with the end of the range and it will be reduced
        prevH1 = 0
        prevH2 = 0
        h1 = tsc1
        h2 = tsc2
        
        #first, find the range boundaries
        while prevH1 != h1:
            prevH1 = h1
            h1 = bwt1.getOccurrenceOfCharAtIndex(x, h1)
        
        #record the h range
        hRanges1_view[x] = h1
        
        #now we need to find the S* counts
        if h1 == tsc1:
            #nothing can be present here
            sCounts1_view[x] = 0
        else:
            if isNumerical1:
                #it's a NumericalBWT, so best to just look at the range and count symbols that qualify
                tempCount = 0
                for y in range(h1, tsc1):
                    if bwt1.getCharAtIndex(y) > x:
                        tempCount += 1
                sCounts1_view[x] = tempCount
            else:
                #it's a BWT, get the FM-index and subtract the delta
                bwt1.fillFmAtIndex(fmIndexSpace1_view, h1)
                bwt1.fillFmAtIndex(fmIndexSpace2_view, tsc1)
                tempCount = 0
                for y in range(x+1, vcLen):
                    tempCount += fmIndexSpace2_view[y]-fmIndexSpace1_view[y]
                sCounts1_view[x] = tempCount
            
        #same thing for the second BWT, find the range boundaries
        while prevH2 != h2:
            prevH2 = h2
            h2 = bwt2.getOccurrenceOfCharAtIndex(x, h2)
        
        #record the h range
        hRanges2_view[x] = h2
        
        #now we need to find the S* counts
        if h2 == tsc2:
            #nothing can be present here
            sCounts2_view[x] = 0
        else:
            if isNumerical2:
                #it's a NumericalBWT, so best to just look at the range and count symbols that qualify
                tempCount = 0
                for y in range(h2, tsc2):
                    if bwt2.getCharAtIndex(y) > x:
                        tempCount += 1
                sCounts2_view[x] = tempCount
            else:
                #it's a BWT, get the FM-index and subtract the delta
                bwt2.fillFmAtIndex(fmIndexSpace1_view, h2)
                bwt2.fillFmAtIndex(fmIndexSpace2_view, tsc2)
                tempCount = 0
                for y in range(x+1, vcLen):
                    tempCount += fmIndexSpace2_view[y]-fmIndexSpace1_view[y]
                sCounts2_view[x] = tempCount
    
    #figure out the start of the counts regions
    #TODO: is it better to use numpy or just fill it in manually?
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] sStarts1 = np.cumsum(sCounts1)-sCounts1
    cdef np.uint64_t [:] sStarts1_view = sStarts1
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] sStarts2 = np.cumsum(sCounts2)-sCounts2
    cdef np.uint64_t [:] sStarts2_view = sStarts2
    
    #third, go through linearly using the forward index to build the new sub-bwt
    #TODO: if we do the above manually, we can fold this in too
    cdef unsigned long ts1 = np.sum(sCounts1)
    cdef unsigned long ts2 = np.sum(sCounts2)
    
    #put the S* indices in a list
    cdef EFA sStarIndices1 = EFA(tsc1, ts1, logger)
    cdef EFA sStarIndices2 = EFA(tsc2, ts2, logger)
    
    #fill in the S* indices into the EFAs
    for x in range(0, vcLen):
        for y in range(hRanges1_view[x], endRanges1_view[x]):
            if bwt1.getCharAtIndex(y) > x:
                sStarIndices1.addValue(y)
        
        for y in range(hRanges2_view[x], endRanges2_view[x]):
            if bwt2.getCharAtIndex(y) > x:
                sStarIndices2.addValue(y)
    
    #this is kind of a hack, but we know there can't be more types of symbols than there are symbols, so use that
    cdef unsigned long newVCLen = ts1+ts2
    '''
    logger.info('Calculating new alphabet length...')
    cdef unsigned long newVCLen = 0
    #cdef list rangeList = []
    rangeList = deque()
    cdef unsigned long l1, l2
    for x in range(0, vcLen):
        for y in range(x+1, vcLen):
            l1 = bwt1.getOccurrenceOfCharAtIndex(y, startRanges1_view[x])
            h1 = bwt1.getOccurrenceOfCharAtIndex(y, endRanges1_view[x])
            l2 = bwt2.getOccurrenceOfCharAtIndex(y, startRanges2_view[x])
            h2 = bwt2.getOccurrenceOfCharAtIndex(y, endRanges2_view[x])
            
            if l1 != h1 or l2 != h2:
                #the first True means we are getting larger right now
                rangeList.append((True, l1, h1, l2, h2, y))
    
    logger.info('init done...')
    cdef bint isL
    cdef unsigned long midPoint
    cdef unsigned long low1, high1, low2, high2
    while len(rangeList) > 0:
        (isL, low1, high1, low2, high2, y) = rangeList.pop()
        if isL:
            midPoint = y
            #first add any Ls
            for x in range(midPoint, vcLen):
                l1 = bwt1.getOccurrenceOfCharAtIndex(x, low1)
                h1 = bwt1.getOccurrenceOfCharAtIndex(x, high1)
                l2 = bwt2.getOccurrenceOfCharAtIndex(x, low2)
                h2 = bwt2.getOccurrenceOfCharAtIndex(x, high2)
                if l1 != h1 or l2 != h2:
                    rangeList.append((True, l1, h1, l2, h2, x))
        else:
            midPoint = y+1
            #first check if any of these are S*, as long as one is we ++
            for x in range(midPoint, vcLen):
                l1 = bwt1.getOccurrenceOfCharAtIndex(x, low1)
                h1 = bwt1.getOccurrenceOfCharAtIndex(x, high1)
                l2 = bwt2.getOccurrenceOfCharAtIndex(x, low2)
                h2 = bwt2.getOccurrenceOfCharAtIndex(x, high2)
                if l1 != h1 or l2 != h2:
                    #only add this once
                    newVCLen += 1
                    break
        
        #now add any Ss
        for x in range(0, midPoint):
            l1 = bwt1.getOccurrenceOfCharAtIndex(x, low1)
            h1 = bwt1.getOccurrenceOfCharAtIndex(x, high1)
            l2 = bwt2.getOccurrenceOfCharAtIndex(x, low2)
            h2 = bwt2.getOccurrenceOfCharAtIndex(x, high2)
            if l1 != h1 or l2 != h2:
                rangeList.append((False, l1, h1, l2, h2, x))
                
    logger.info('New alphabet length:\t'+str(newVCLen))
    '''
    
    logger.info('New calculated sizes:\t'+str(ts1)+'\t'+str(ts2))
    cdef NumericalBWT b1 = NumericalBWT()
    b1.allocateMsbwt(newVCLen, ts1, logger)
    
    cdef NumericalBWT b2 = NumericalBWT()
    b2.allocateMsbwt(newVCLen, ts2, logger)
    
    #now we go through them both linearly
    cdef unsigned long currVCValue = 0
    
    cdef unsigned long ind1, ind2
    cdef unsigned long sFound1, sFound2
    cdef list sStarID1, sStarID2, prevSym
    cdef bint unfound
    cdef unsigned long writeInd
    cdef unsigned long nextInd1, nextInd2
    cdef unsigned long nextSym1, nextSym2
    
    for x in range(0, vcLen):
        #print 'alloc loop', x, vcLen, sCounts1_view[x]+sCounts2_view[x]
        ind1 = hRanges1_view[x]
        sFound1 = 0
        
        #print x, sCounts1_view[x], sCounts2_view[x]
        
        if sFound1 >= sCounts1_view[x]:
            sStarID1 = [0xFFFFFFFFFFFFFFFF]
        else:
            unfound = True
            while unfound:
                sym = bwt1.getCharAtIndex(ind1)
                if sym > x:
                    #now build up the tuple
                    (sStarID1, nextInd1, nextSym1) = buildSStar(bwt1, ind1, startRanges1_view, endRanges1_view, 
                                                                hRanges1_view, forwardIndices1, vcLen)
                    
                    #this is an S* value
                    sFound1 += 1
                    unfound = False
                
                ind1 += 1
        
        ind2 = hRanges2_view[x]
        sFound2 = 0
        if sFound2 >= sCounts2_view[x]:
            sStarID2 = [0xFFFFFFFFFFFFFFFF]
        else:
            unfound = True
            while unfound:
                sym = bwt2.getCharAtIndex(ind2)
                if sym > x:
                    #now build up the tuple
                    (sStarID2, nextInd2, nextSym2) = buildSStar(bwt2, ind2, startRanges2_view, endRanges2_view, 
                                                                hRanges2_view, forwardIndices2, vcLen)
                    
                    #this is an S* value
                    sFound2 += 1
                    unfound = False
                
                ind2 += 1
        
        #start with the small one
        if sStarID1 <= sStarID2:
            prevSym = sStarID1
        else:
            prevSym = sStarID2
            
        for y in range(0, sCounts1_view[x]+sCounts2_view[x]):
            if sStarID1 <= sStarID2:
                #pick sStarID1 if it's smaller or they're the same
                #first, figure out the position in the new BWT to write
                writeInd = sStarIndices1.countLessThanValue(nextInd1)
                
                if sStarID1 > prevSym:
                    #print prevSym
                    currVCValue += 1
                    if currVCValue % 1000 == 0:
                        logger.info('Found '+str(currVCValue/1000)+'K symbols, '+str(sStarID1)+'...')
                    prevSym = sStarID1
                
                b1.presetValueAtIndex(currVCValue, writeInd)
                
                if sFound1 >= sCounts1_view[x]:
                    sStarID1 = [0xFFFFFFFFFFFFFFFF]
                else:
                    unfound = True
                    while unfound:
                        sym = bwt1.getCharAtIndex(ind1)
                        if sym > x:
                            #now build up the tuple
                            (sStarID1, nextInd1, nextSym1) = buildSStar(bwt1, ind1, startRanges1_view, endRanges1_view, 
                                                                        hRanges1_view, forwardIndices1, vcLen)
                            
                            #this is an S* value
                            sFound1 += 1
                            unfound = False
                        
                        ind1 += 1
                
            else:
                #pick sStarID2
                #first, figure out the position in the new BWT to write
                writeInd = sStarIndices2.countLessThanValue(nextInd2)
                
                if sStarID2 > prevSym:
                    #print prevSym
                    currVCValue += 1
                    if currVCValue % 1000 == 0:
                        logger.info('Found '+str(currVCValue/1000)+'K symbols, '+str(sStarID2)+'...')
                    prevSym = sStarID2
                
                b2.presetValueAtIndex(currVCValue, writeInd)
                
                if sFound2 >= sCounts2_view[x]:
                    sStarID2 = [0xFFFFFFFFFFFFFFFF]
                else:
                    unfound = True
                    while unfound:
                        sym = bwt2.getCharAtIndex(ind2)
                        if sym > x:
                            #now build up the tuple
                            (sStarID2, nextInd2, nextSym2) = buildSStar(bwt2, ind2, startRanges2_view, endRanges2_view, 
                                                                        hRanges2_view, forwardIndices2, vcLen)
                            
                            #this is an S* value
                            sFound2 += 1
                            unfound = False
                        
                        ind2 += 1
        
        #advance this counter so long as something was S* in this symbol range
        if sCounts1_view[x]+sCounts2_view[x] > 0:
            #print prevSym
            currVCValue += 1
            if currVCValue % 1000 == 0:
                logger.info('Found '+str(currVCValue/1000)+'K symbols, '+str(prevSym)+'...')
    
    #print 'newVcLen', newVCLen, currVCValue, (ts1+ts2)
    logger.info('Estimated alphabet size:\t'+str(newVCLen))
    logger.info('True alphabet size:\t'+str(currVCValue))
    
    #clear up some memory before we create all the final indices
    sStarIndices1 = None
    sStarIndices2 = None
    
    #finish the allocation of these values
    b1.finalizeAllocate(currVCValue, logger)
    b2.finalizeAllocate(currVCValue, logger)
    
    #four, return the BWTS?
    return (b1, b2, currVCValue)

cdef inline tuple buildSStar(BasicBWT bwt, unsigned long startingIndex, np.uint64_t [:] startRanges, np.uint64_t [:] endRanges,
                             np.uint64_t [:] hRanges, list forwardIndices, unsigned long vcLen):
    #cdef unsigned long prevSym = np.searchsorted(endRanges, startingIndex, 'right')
    cdef unsigned long prevSym = searchSortedRight(endRanges, vcLen, startingIndex)
    cdef unsigned long prevInd
    cdef list ret = []
    
    cdef unsigned long ind# = (<EFA>forwardIndices[prevSym]).getValueAtIndex(startingIndex-startRanges[prevSym])
    #if endRanges[prevSym] - startRanges[prevSym] > 20:
    if isinstance(forwardIndices[prevSym], EFA):
        ind = (<EFA>forwardIndices[prevSym]).getValueAtIndex(startingIndex-startRanges[prevSym])
    else:
        ind = (<list>forwardIndices[prevSym])[startingIndex-startRanges[prevSym]]
    cdef unsigned long sym = searchSortedRight(endRanges, vcLen, ind)
    
    while ind >= hRanges[sym]:
    #while sym >= prevSym:
        ret.append(prevSym)
        
        prevSym = sym
        prevInd = ind
        #if endRanges[sym] - startRanges[sym] > 20:
        if isinstance(forwardIndices[sym], EFA):
            ind = (<EFA>forwardIndices[sym]).getValueAtIndex(ind-startRanges[sym])
        else:
            ind = (<list>forwardIndices[sym])[ind-startRanges[sym]]
        sym = searchSortedRight(endRanges, vcLen, ind)
    
    while ind < hRanges[sym]:
        ret.append(prevSym)
        
        prevSym = sym
        prevInd = ind
        #if endRanges[sym] - startRanges[sym] > 20:
        if isinstance(forwardIndices[sym], EFA):
            ind = (<EFA>forwardIndices[sym]).getValueAtIndex(ind-startRanges[sym])
        else:
            ind = (<list>forwardIndices[sym])[ind-startRanges[sym]]
        sym = searchSortedRight(endRanges, vcLen, ind)
    
    ret.append(prevSym)
    ret.append(sym)
    ret.append(0xFFFFFFFFFFFFFFFF)
    #return (ret, prevInd, prevSym)
    return (ret, ind, sym)

cdef inline unsigned long searchSortedRight(np.uint64_t [:] searchList, unsigned long listLen, unsigned long searchValue):
    cdef unsigned long l = 0
    cdef unsigned long h = listLen
    cdef unsigned long m
    while l != h:
        m = (l+h)/2
        if searchList[m] <= searchValue:
            l = m+1
        else:
            h = m
    return l

cdef bint symbolShare(BasicBWT b1, BasicBWT b2, unsigned long vcLen):
    cdef unsigned long x
    for x in range(0, vcLen):
        if b1.getSymbolCount(x) > 0 and b2.getSymbolCount(x) > 0:
            return True
    
    return False

cdef tuple findSingleSymbolBounds(BasicBWT bwt, unsigned long symbol):
    cdef unsigned long prevL = 0
    cdef unsigned long prevH = 0
    
    cdef unsigned long l = 0
    cdef unsigned long h = bwt.getTotalSize()
    
    while prevL != l or prevH != h:
        prevL = l
        prevH = h
        l = bwt.getOccurrenceOfCharAtIndex(symbol, l)
        h = bwt.getOccurrenceOfCharAtIndex(symbol, h)
    
    return (l, h)

cdef void interleaveBwts(BasicBWT bwt1, BasicBWT bwt2, np.uint8_t [:] interleave, char * outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    outputFn = outputDir+'/msbwt.npy'
    
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] bwtOut = np.lib.format.open_memmap(outputFn, 'w+', '<u1', (bwt1.getTotalSize()+bwt2.getTotalSize(), ))
    cdef np.uint8_t [:] bwtOut_view = bwtOut
    
    cdef unsigned long ind1 = 0
    cdef unsigned long ind2 = 0
    cdef unsigned long x
    for x in range(0, bwtOut.shape[0]):
        #if interleave[x]:
        if getBit(interleave, x):
            bwtOut_view[x] = bwt2.getCharAtIndex(ind2)
            ind2 += 1
        else:
            bwtOut_view[x] = bwt1.getCharAtIndex(ind1)
            ind1 += 1

cdef inline void setBit(np.uint8_t [:] bitArray, unsigned long index) nogil:
    #set a bit in an array
    bitArray[index >> 3] |= (0x1 << (index & 0x7))
    
cdef inline bint getBit(np.uint8_t [:] bitArray, unsigned long index) nogil:
    #get a bit from an array
    return (bitArray[index >> 3] >> (index & 0x7)) & 0x1