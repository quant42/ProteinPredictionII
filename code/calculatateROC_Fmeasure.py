#!/usr/bin/env python

validationResults = '../data/validationResults'

def fMeasure(validationResults, steps=10):
    maxConf = -99999
    minConf = +99999
    
    for line in open(validationResults):
        if line.startswith('*'):
            continue
        HPOterm, confidence, validation = line.split()
        if float(confidence) > maxConf:
            maxConf = float(confidence)
        elif float(confidence) < minConf:
            minConf = float(confidence)

    F_max = 0
    for i in range(steps+1):
        confidenceLevel = (1.0/steps)*i
        print 'min confidence:', confidenceLevel
        TP, FP, FN = 0, 0, 0        
        for line in open(validationResults):
            if line.startswith('*'):
                FN += int(line.split('=')[1].split(')')[0])
                continue
        
            HPOterm, confidence, validation = line.split()
            confidence = (float(confidence) - minConf)/(maxConf-minConf)
            
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
            precision = float(TP)/(TP+FP)
            recall = float(TP)/(TP+FN)
            print precision, recall
        except:
            print TP, FP, FN
        try:
            f = (2.0*precision*recall)/(precision+recall)
            if f > F_max:
                F_max = f
            
        except Exception:
            pass
    return F_max
f_max = fMeasure(validationResults, steps=10)
print "F-measure =", f_max
