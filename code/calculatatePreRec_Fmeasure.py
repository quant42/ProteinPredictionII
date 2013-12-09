#!/usr/bin/env python
import sys
validationResults = '../data/validationResults_5'
hpoMappingFile = '../data/UniProt_2_HPO_full'

def fMeasure(validationResults, steps=10):
    uni2hpoDict = {}
    f = open(hpoMappingFile)
    for line in f:
        line = line.strip()
        uni2hpoDict.update( { line.split("\t")[0] : line.split("\t")[1].split(",") } )
    f.close()
    
    maxConf = -99999
    minConf = +99999

    ROCpoints = []
    
    for line in open(validationResults):
        if line.startswith('*'):
            continue
        Sequence, HPOterm, confidence, validation = line.split()
        if float(confidence) > maxConf:
            maxConf = float(confidence)
        elif float(confidence) < minConf:
            minConf = float(confidence)
    F_max = 0
    pre_max = 0
    rec_max = 0
    for i in range(steps+1):
        confidenceLevel = (1.0/steps)*i
        precisions = []
        recalls = []
        TP, FP, FN = 0, 0, 0
        thisSequence = ''
        for line in open(validationResults):
            if line.startswith('*'):
                continue
        
            Sequence, HPOterm, confidence, validation = line.split()
            confidence = (float(confidence) - minConf)/(maxConf-minConf)

            if thisSequence != Sequence:                
                if thisSequence:                 
                    FN += len(uni2hpoDict[thisSequence])-TP
                    
                    try:
                        thisPrec   = float(TP)/(TP+FP)
                    except:
                        thisPrec = 0
                    thisRecall = float(TP)/(TP+FN)
                    
                    if thisPrec != 0:
                        precisions.append(thisPrec)
                    recalls.append(thisRecall)
                thisSequence = Sequence
                TP, FP, FN = 0, 0, 0
                
            if confidence >= confidenceLevel:
                if validation.strip() == 'True':
                    TP += 1
                else:
                    FP += 1
            else:
                if validation.strip() == 'True':
                    FN += 1
        #print TP, FP, FN
                    
        try:
            precision = sum(precisions)/len(precisions)
        except:
            precision = 0
        recall = sum(recalls)/len(recalls)
        ROCpoints.append((recall,precision))
        try:
            f = (2.0*precision*recall)/(precision+recall)
            if f > F_max:
                F_max = f
                pre_max = precision
                rec_max = recall
        except Exception:
            pass
    return (F_max, pre_max, rec_max), ROCpoints
f_max, ROCpoints = fMeasure(validationResults, steps=10)
print "F-measure, precision and recall at same confidence =", f_max
for rec, pre in ROCpoints:
    print "%s;%s"%(rec, pre)
