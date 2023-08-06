#!python
#cython: boundscheck=False
#cython: wraparound=False

from BasicBWT cimport BasicBWT
from EliasFanoArray cimport EliasFanoArray as EFA

import numpy as np
cimport numpy as np

#from libcpp.deque cimport deque
from collections import deque

def identifyLMS(BasicBWT bwt1, BasicBWT bwt2, unsigned long vcLen, logger):
    '''
    TODO
    '''
    #cdef deque[EFA] test
    
    #cdef list initList = []
    initList = deque()
    cdef unsigned long origL = 0
    cdef unsigned long origH1 = bwt1.getTotalSize()
    cdef unsigned long origH2 = bwt2.getTotalSize()
    cdef unsigned long prevl, prevh, l1, h1, l2, h2
    
    cdef unsigned long tsc1 = 0
    cdef unsigned long tsc2 = 0
    cdef unsigned long sCount1 = 0
    cdef unsigned long sCount2 = 0
    
    cdef EFA ind1, ind2
    
    cdef unsigned long x, y
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmIndex1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.uint64_t [:] fmIndex1_view = fmIndex1
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmIndex2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.uint64_t [:] fmIndex2_view = fmIndex2
    
    for x in range(0, vcLen):
        #move the total symbol count
        tsc1 += bwt1.getSymbolCount(x)
        tsc2 += bwt2.getSymbolCount(x)
        
        #figure out where a seq like 'AAAAAAAA...' would be in bwt1
        prevl = origL
        l1 = origL
        prevh = 0
        h1 = origH1
        while prevl != l1 or prevh != h1:
            prevl = l1
            prevh = h1
            #l1 = bwt1.getFullFMAtIndex(l1)[x]
            #h1 = bwt1.getFullFMAtIndex(h1)[x]
            bwt1.fillFmAtIndex(fmIndex1_view, l1)
            l1 = fmIndex1_view[x]
            bwt1.fillFmAtIndex(fmIndex1_view, h1)
            h1 = fmIndex1_view[x]
            
        #figure out where a seq like 'AAAAAAAA...' would be in bwt2
        prevl = origL
        l2 = origL
        prevh = 0
        h2 = origH2
        while prevl2 != l2 or prevh2 != h2:
            prevl2 = l2
            prevh2 = h2
            #l2 = bwt2.getFullFMAtIndex(l2)[x]
            #h2 = bwt2.getFullFMAtIndex(h2)[x]
            bwt2.fillFmAtIndex(fmIndex2_view, l2)
            l2 = fmIndex2_view[x]
            bwt2.fillFmAtIndex(fmIndex2_view, h2)
            h2 = fmIndex2_view[x]
        
        #store the list of all S strings
        if h1 != tsc1 or h2 != tsc2:
            ind1 = EFA(tsc1, tsc1-h1)
            for y in range(h1, tsc1):
                if bwt1.getCharAtIndex(y) > x:
                    ind1.addValue(y)
            
            ind2 = EFA(tsc2, tsc2-h2)
            for y in range(h2, tsc2):
                if bwt2.getCharAtIndex(y) > x:
                    ind2.addValue(y)
            
            initList.append(([x], h1, tsc1, h2, tsc2, ind1, ind2))
    
    #print 'initList', initList
    logger.info('identifyLMS: init built')
    #cdef list LList = []
    LList = deque()
    cdef tuple tup
    cdef list seq
    cdef unsigned long firstSym
    cdef unsigned long si1, ei1, si2, ei2
    cdef EFA efaReader1, efaReader2
    
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmStart1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmEnd1 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmStart2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    cdef np.ndarray[np.uint64_t, ndim=1, mode='c'] fmEnd2 = np.zeros(dtype='<u8', shape=(vcLen, ))
    
    cdef np.uint64_t [:] fmStart1_view = fmStart1
    cdef np.uint64_t [:] fmEnd1_view = fmEnd1
    cdef np.uint64_t [:] fmStart2_view = fmStart2
    cdef np.uint64_t [:] fmEnd2_view = fmEnd2
    
    cdef dict ind1SubLists, ind2SubLists
    cdef unsigned long v
    for tup in initList:
        seq = tup[0]
        firstSym = seq[0]
        
        si1 = tup[1]
        ei1 = tup[2]
        si2 = tup[3]
        ei2 = tup[4]
        efaReader1 = tup[5]
        efaReader2 = tup[6]
        
        bwt1.fillFmAtIndex(fmStart1_view, si1)
        bwt1.fillFmAtIndex(fmEnd1_view, ei1)
        bwt2.fillFmAtIndex(fmStart2_view, si2)
        bwt2.fillFmAtIndex(fmEnd2_view, ei2)
        
        #ind1SubLists = [EFA(tsc1, fmEnd1_view[x]-fmStart1_view[x], 1) if (fmEnd1_view[x]-fmStart1_view[x] > 0) else None for x in range(0, vcLen)]
        ind1SubLists = {}
        for x in range(0, vcLen):
            if fmEnd1_view[x]-fmStart1_view[x] > 0:
                ind1SubLists[x] = EFA(tsc1, fmEnd1_view[x]-fmStart1_view[x])
        
        efaReader1.resetReader()
        for x in range(0, efaReader1.getNumValues()):
            v = efaReader1.decodeValue()
            (<EFA>ind1SubLists[bwt1.getCharAtIndex(v)]).addValue(sCount1)
            sCount1 += 1
        
        #ind2SubLists = [EFA(tsc2, fmEnd2_view[x]-fmStart2_view[x], 1) if (fmEnd2_view[x]-fmStart2_view[x] > 0) else None for x in range(0, vcLen)]
        ind2SubLists = {}
        for x in range(0, vcLen):
            if fmEnd2_view[x]-fmStart2_view[x] > 0:
                ind2SubLists[x] = EFA(tsc2, fmEnd2_view[x]-fmStart2_view[x])
        
        efaReader2.resetReader()
        for x in range(0, efaReader2.getNumValues()):
            v = efaReader2.decodeValue()
            (<EFA>ind2SubLists[bwt2.getCharAtIndex(v)]).addValue(sCount2)
            sCount2 += 1
        
        #we need the element before to be greater than the first symbol
        for x in range(firstSym+1, vcLen):
            if fmStart1_view[x] != fmEnd1_view[x] or fmStart2_view[x] != fmEnd2_view[x]:
                #LList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists[x], ind2SubLists[x]))
                LList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists.get(x, None), ind2SubLists.get(x, None)))
    
    #clear the initial list
    initList = None
    
    #print 'first LList', LList
    logger.info('identifyLMS: LList built')
    
    #cdef list SList = []
    SList = deque()
    while len(LList) > 0:
        tup = LList.pop()
        seq = tup[0]
        firstSym = seq[0]
        
        si1 = tup[1]
        ei1 = tup[2]
        si2 = tup[3]
        ei2 = tup[4]
        
        bwt1.fillFmAtIndex(fmStart1_view, si1)
        bwt1.fillFmAtIndex(fmEnd1_view, ei1)
        bwt2.fillFmAtIndex(fmStart2_view, si2)
        bwt2.fillFmAtIndex(fmEnd2_view, ei2)
        
        efaReader1 = tup[5]
        efaReader2 = tup[6]
        
        #ind1SubLists = [EFA(tsc1, fmEnd1_view[x]-fmStart1_view[x], 1) if (fmEnd1_view[x]-fmStart1_view[x] > 0) else None for x in range(0, vcLen)]
        ind1SubLists = {}
        for x in range(0, vcLen):
            if fmEnd1_view[x]-fmStart1_view[x] > 0:
                #ind1SubLists[x] = EFA(tsc1, fmEnd1_view[x]-fmStart1_view[x], 1)
                ind1SubLists[x] = EFA(sCount1, fmEnd1_view[x]-fmStart1_view[x])
        
        if efaReader1:
            efaReader1.resetReader()
            for x in range(0, efaReader1.getNumValues()):
                v = efaReader1.decodeValue()
                (<EFA>ind1SubLists[bwt1.getCharAtIndex(si1+x)]).addValue(v)
        
        #ind2SubLists = [EFA(tsc2, fmEnd2_view[x]-fmStart2_view[x], 1) if (fmEnd2_view[x]-fmStart2_view[x] > 0) else None for x in range(0, vcLen)]
        ind2SubLists = {}
        for x in range(0, vcLen):
            if fmEnd2_view[x]-fmStart2_view[x] > 0:
                #ind2SubLists[x] = EFA(tsc2, fmEnd2_view[x]-fmStart2_view[x], 1)
                ind2SubLists[x] = EFA(sCount2, fmEnd2_view[x]-fmStart2_view[x])
        
        if efaReader2:
            efaReader2.resetReader()
            for x in range(0, efaReader2.getNumValues()):
                v = efaReader2.decodeValue()
                (<EFA>ind2SubLists[bwt2.getCharAtIndex(si2+x)]).addValue(v)
        
        #we add to the SList if the element before is less than
        for x in range(0, firstSym):
            if fmStart1_view[x] != fmEnd1_view[x] or fmStart2_view[x] != fmEnd2_view[x]:
                #SList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists[x], ind2SubLists[x]))
                SList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists.get(x, None), ind2SubLists.get(x, None)))
        
        #we add to the LList if the element before is greater than OR equal to
        for x in range(firstSym, vcLen):
            if fmStart1_view[x] != fmEnd1_view[x] or fmStart2_view[x] != fmEnd2_view[x]:
                #LList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists[x], ind2SubLists[x]))
                LList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists.get(x, None), ind2SubLists.get(x, None)))
    
    #print 'SList', SList
    logger.info('identifyLMS: SList built')
    
    #cdef list LMSList = []
    LMSList = deque()
    cdef EFA extraArray1, extraArray2
    cdef unsigned long sym
    cdef bint extraElements
    cdef unsigned long totalExtra1, totalExtra2
    
    while len(SList) > 0:
        tup = SList.pop()
        seq = tup[0]
        firstSym = seq[0]
        
        si1 = tup[1]
        ei1 = tup[2]
        si2 = tup[3]
        ei2 = tup[4]
        
        bwt1.fillFmAtIndex(fmStart1_view, si1)
        bwt1.fillFmAtIndex(fmEnd1_view, ei1)
        bwt2.fillFmAtIndex(fmStart2_view, si2)
        bwt2.fillFmAtIndex(fmEnd2_view, ei2)
        
        efaReader1 = tup[5]
        efaReader2 = tup[6]
        
        #ind1SubLists = [EFA(tsc1, fmEnd1_view[x]-fmStart1_view[x], 1) if (fmEnd1_view[x]-fmStart1_view[x] > 0) else None for x in range(0, firstSym+1)]
        ind1SubLists = {}
        for x in range(0, vcLen):
            if fmEnd1_view[x]-fmStart1_view[x] > 0:
                #ind1SubLists[x] = EFA(tsc1, fmEnd1_view[x]-fmStart1_view[x], 1)
                ind1SubLists[x] = EFA(sCount1, fmEnd1_view[x]-fmStart1_view[x])
        
        #extraArray1 = EFA(tsc1, np.sum(fmEnd1[firstSym+1:])-np.sum(fmStart1[firstSym+1:]), 1)
        extraArray1 = EFA(sCount1, np.sum(fmEnd1[firstSym+1:])-np.sum(fmStart1[firstSym+1:]))
        if efaReader1:
            efaReader1.resetReader()
            for x in range(0, efaReader1.getNumValues()):
                v = efaReader1.decodeValue()
                sym = bwt1.getCharAtIndex(si1+x)
                if sym > firstSym:
                    extraArray1.addValue(v)
                else:
                    (<EFA>ind1SubLists[sym]).addValue(v)
        
        #ind2SubLists = [EFA(tsc2, fmEnd2[x]-fmStart2[x], 1) for x in xrange(0, vcLen)]
        #ind2SubLists = [EFA(tsc2, fmEnd2_view[x]-fmStart2_view[x], 1) if (fmEnd2_view[x]-fmStart2_view[x] > 0) else None for x in range(0, firstSym+1)]
        ind2SubLists = {}
        for x in range(0, vcLen):
            if fmEnd2_view[x]-fmStart2_view[x] > 0:
                #ind2SubLists[x] = EFA(tsc2, fmEnd2_view[x]-fmStart2_view[x], 1)
                ind2SubLists[x] = EFA(sCount2, fmEnd2_view[x]-fmStart2_view[x])
        
        #extraArray2 = EFA(tsc2, np.sum(fmEnd2[firstSym+1:])-np.sum(fmStart2[firstSym+1:]), 1)
        extraArray2 = EFA(sCount2, np.sum(fmEnd2[firstSym+1:])-np.sum(fmStart2[firstSym+1:]))
        if efaReader2:
            efaReader2.resetReader()
            for x in range(0, efaReader2.getNumValues()):
                v = efaReader2.decodeValue()
                sym = bwt2.getCharAtIndex(si2+x)
                if sym > firstSym:
                    extraArray2.addValue(v)
                else:
                    (<EFA>ind2SubLists[sym]).addValue(v)
        
        #we add to the SList if the element before is less than OR equal to
        for x in range(0, firstSym+1):
            if fmStart1_view[x] != fmEnd1_view[x] or fmStart2_view[x] != fmEnd2_view[x]:
                #SList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists[x], ind2SubLists[x]))
                SList.append(([x]+seq, fmStart1_view[x], fmEnd1_view[x], fmStart2_view[x], fmEnd2_view[x], ind1SubLists.get(x, None), ind2SubLists.get(x, None)))
        
        #we add to the LList if the element before is greater than
        extraElements = False
        totalExtra1 = 0
        totalExtra2 = 0
        for x in range(firstSym+1, vcLen):
            if fmStart1_view[x] != fmEnd1_view[x] or fmStart2_view[x] != fmEnd2_view[x]:
                #LMSList.append((seq, tup[1], tup[2], tup[3], tup[4], ind1SubLists[x], ind2SubLists[x]))
                extraElements = True
                totalExtra1 += fmEnd1_view[x]-fmStart1_view[x]
                totalExtra2 += fmEnd2_view[x]-fmStart2_view[x]
        
        if extraElements:
            #firstList = extraArray1
            #secondList = extraArray2
            
            LMSList.append((seq, tup[1], tup[2], tup[3], tup[4], extraArray1, extraArray2))
    
    logger.info('identifyLMS: LMSList built')
    
    cdef list LMSList2 = list(LMSList)
    LMSList2.sort(key=lambda x: (x[1], x[3], x[2], x[4]))
    logger.info('identifyLMS: LMSList sorted')
    
    #print 'LMSList', LMSList
    #print 'len of LMSList', len(LMSList)
    #print 'lms coverage', sum([tup[2]-tup[1]+tup[4]-tup[3] for tup in LMSList])
    
    return reduceLMSList(LMSList2, sCount1, sCount2)

cdef tuple reduceLMSList(list LMSList, unsigned long sCount1, unsigned long sCount2):
    #print LMSList
    
    cdef list tupleList = []
    cdef list LMSList1 = []
    cdef list LMSList2 = []
    
    if len(LMSList) == 0:
        return ([], [], [])
    
    #cdef tuple currentLMSTup = LMSList[0]
    cdef tuple currentLMSTup = LMSList.pop(0)
    cdef list currentID = currentLMSTup[0]
    cdef list currentEFAs1 = [currentLMSTup[5]]
    cdef list currentEFAs2 = [currentLMSTup[6]]
    
    cdef unsigned long x, y, z
    
    cdef list listID = currentID
    
    cdef unsigned long tc1, tc2
    cdef EFA newEFA1, newEFA2
    cdef EFA cEFA
    
    #for x in range(1, len(LMSList)):
    while len(LMSList) > 0:
        #currentLMSTup = LMSList[x]
        currentLMSTup = LMSList.pop(0)
        currentID = currentLMSTup[0]
        
        if currentID[0:len(currentID)-1] == listID[0:len(listID)-1]:
            #same symbol, append
            #currentEFAs1.append(LMSList[x][5])
            #currentEFAs2.append(LMSList[x][6])
            currentEFAs1.append(currentLMSTup[5])
            currentEFAs2.append(currentLMSTup[6])
        else:
            tc1 = 0
            tc2 = 0
            for y in range(0, len(currentEFAs1)):
                tc1 += (<EFA>currentEFAs1[y]).getNumValues()
                tc2 += (<EFA>currentEFAs2[y]).getNumValues()
            
            newEFA1 = EFA(sCount1, tc1)
            newEFA2 = EFA(sCount2, tc2)
            
            for y in range(0, len(currentEFAs1)):
                cEFA = currentEFAs1[y]
                cEFA.resetReader()
                for z in range(0, cEFA.getNumValues()):
                    newEFA1.addValue(cEFA.decodeValue())
                
                cEFA = currentEFAs2[y]
                cEFA.resetReader()
                for z in range(0, cEFA.getNumValues()):
                    newEFA2.addValue(cEFA.decodeValue())
            
            #retLMSList.append((currentID[0:-1], newEFA1, newEFA2))
            tupleList.append(currentID[0:len(currentID)-1])
            LMSList1.append(newEFA1)
            LMSList2.append(newEFA2)
            
            #different symbol, append
            listID = currentID
            currentEFAs1 = [currentLMSTup[5]]
            currentEFAs2 = [currentLMSTup[6]]
    
    #do this for the last set
    tc1 = 0
    tc2 = 0
    for y in range(0, len(currentEFAs1)):
        tc1 += (<EFA>currentEFAs1[y]).getNumValues()
        tc2 += (<EFA>currentEFAs2[y]).getNumValues()
    
    newEFA1 = EFA(sCount1, tc1)
    newEFA2 = EFA(sCount2, tc2)
    
    for y in range(0, len(currentEFAs1)):
        cEFA = currentEFAs1[y]
        cEFA.resetReader()
        for z in range(0, cEFA.getNumValues()):
            newEFA1.addValue(cEFA.decodeValue())
        
        cEFA = currentEFAs2[y]
        cEFA.resetReader()
        for z in range(0, cEFA.getNumValues()):
            newEFA2.addValue(cEFA.decodeValue())
    
    #retLMSList.append((currentID[0:-1], newEFA1, newEFA2))
    tupleList.append(currentID[0:len(currentID)-1])
    LMSList1.append(newEFA1)
    LMSList2.append(newEFA2)
    
    return (tupleList, LMSList1, LMSList2)
