#!/usr/bin/env python
import sys, numpy
validationResults = '../data/validationResults_'
hpoMappingFile = '../data/UniProt_2_HPO_full'

def fMeasure(validationResults, steps):
    uni2hpoDict = {}
    f = open(hpoMappingFile)
    for line in f:
        line = line.strip()
        uni2hpoDict.update( { line.split("\t")[0] : line.split("\t")[1].split(",") } )
    f.close()

    maxConf, minConf = Confidence(validationResults)

    ROCpoints = []
    F_max = 0
    pre_max = 0
    rec_max = 0
    conf_max = -1
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
                conf_max = confidenceLevel
        except Exception:
            pass
    return (F_max, pre_max, rec_max, conf_max), ROCpoints

def Confidence(validationResults):
    maxC = -9999
    minC = 9999
    for line in open(validationResults):
        if line.startswith('*'):
            continue
        Sequence, HPOterm, confidence, validation = line.split()
        if float(confidence) > maxC:
            maxC = float(confidence)
        elif float(confidence) < minC:
            minC = float(confidence)
    return maxC, minC

def mean_stdev(data):
    a = 1.0*numpy.array(data)
    n = len(a)
    m, sd = numpy.mean(a), numpy.std(a)    
    return m, sd

steps = 100
f_max, prec, rec = [],[],[]

Precisions = [[] for i in range(steps+1)]
Recalls = [[] for i in range(steps+1)]
   

for i in [11,12,13]:
    f, PreRecPoints = fMeasure(validationResults+str(i), steps)
    f_max.append(f[0])
    prec.append(f[1])
    rec.append(f[2])
    for j in range(len(PreRecPoints)):
        Precisions[j].append(PreRecPoints[j][1])
        Recalls[j].append(PreRecPoints[j][0])
    print "F-measure, precision and recall at same confidence =", f


mean_f, stdev_f = mean_stdev(f_max)
mean_pre, stdev_pre = mean_stdev(prec)
mean_rec, stdev_rec = mean_stdev(rec)
print "avg F-max:     %0.4f+/-%0.4f"%(mean_f, stdev_f)
print "avg precision: %0.4f+/-%0.4f"%(mean_pre, stdev_pre)
print "avg recall:    %0.4f+/-%0.4f"%(mean_rec, stdev_rec)

for i in range(steps+1):
    avg_recall    , std_recall    = mean_stdev(Recalls[i])
    avg_precision ,std_precisions = mean_stdev(Precisions[i])
    print "%s;%s"%(avg_recall, avg_precision)


