#! /usr/bin/env python

# This file is about testing, feature selecting etc. for the neuronal network

### features functions ###

# Feature: the best hit E-Value
def featMaxEValue(graph, node):
  maxEVal = None
  for attr in node.attributes:
    attrEVal = attr[ "hit_value" ]
    if maxEVal == None:
      maxEVal = attrEVal
    else:
      maxEVal = max(maxEVal, attrEVal)
  return maxEVal

# Feature: the number of hits
def featCHits(graph, node):
  return len(node.attributes)

# Feature: the average E-Value
def featAvgEValue(graph, node):
  cAttrs, sumAttrEVal = len(node.attributes), 0.0
  for attr in node.attributes:
    sumAttrEVal += attr[ "hit_value" ]
  return sumAttrEVal / cAttrs

# Feature: The best hit value
def featMaxEValueHitLength(graph, node):
  maxEVal, maxHitLength = None, 0
  for attr in node.attributes:
    attrEVal = attr[ "hit_value" ]
    attrHitLength = attr[ "hit_to" ] + 1 - attr[ "hit_from" ]
    if maxEVal == None:
      maxEVal, maxHitLength = attrEVal, attrHitLength
    elif maxEVal < attrEVal:
      maxEVal, maxHitLength = attrEVal, attrHitLength
  return maxHitLength

### end features functions ###
### feature config ###

features = [ featMaxEValue, featCHits ]

### end feature config ###
### imports ###

from Bio import SeqIO
from random import shuffle
from pybrain.tools.shortcuts import buildNetwork
import multiprocessing

### end imports ###
### some variables ###

threads = multiprocessing.cpu_count() # get the number of cpus to calc simultanly
cFeatures = len(features)
neuronalNetwork = buildNetwork( cFeatures, cFeatures + 1, 3, 1)

### end some variables ###

def trainNetwork

def crossVal(sequences, prozTrain=80, folds=100, threads=4):
  
  for f in features:
    f()

crossVal(None)
