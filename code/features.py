#! /usr/bin/env python

# ok, this is a file containing all features that will be used by the predictor.py to predict if the hpo term is correct for this sequence or not
# note, that all feature functions starts with feat

def featMaxEValue(predictor, self, node, graph, querySequence):
  maxEVal = None
  for attr in node.attributes:
    attrEVal = attr[ "hit_value" ]
    if maxEVal == None:
      maxEVal = attrEVal
    else:
      maxEVal = max(maxEVal, attrEVal)
  return maxEVal

# Feature: the number of hits
def featCHits(predictor, self, node, graph, querySequence):
  return len(node.attributes)

# Feature: the average E-Value
def featAvgEValue(predictor, self, node, graph, querySequence):
  cAttrs, sumAttrEVal = len(node.attributes), 0.0
  for attr in node.attributes:
    sumAttrEVal += attr[ "hit_value" ]
  return sumAttrEVal / cAttrs

# Feature: The best hit value
def featMaxEValueHitLength(predictor, self, node, graph, querySequence):
  maxEVal, maxHitLength = None, 0
  for attr in node.attributes:
    attrEVal = attr[ "hit_value" ]
    attrHitLength = attr[ "hit_to" ] + 1 - attr[ "hit_from" ]
    if maxEVal == None:
      maxEVal, maxHitLength = attrEVal, attrHitLength
    elif maxEVal < attrEVal:
      maxEVal, maxHitLength = attrEVal, attrHitLength
  return maxHitLength

# some helper functions, for the feature functions
def foo():
  pass


