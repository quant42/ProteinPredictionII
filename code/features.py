#! /usr/bin/env python

# ok, this is a file containing all features that will be used by the predictor.py to predict if the hpo term is correct for this sequence or not
# note, that all feature functions starts with feat

def featMaxEValue(predictor, node, graph, querySequence):
  maxEVal = None
  for hit, attr in node.attributes.iteritems():
    attrEVal = attr[ "hit_value" ]
    if maxEVal == None:
      maxEVal = attrEVal
    else:
      maxEVal = max(maxEVal, attrEVal)
  return maxEVal

# Feature: the number of hits
def featCHits(predictor, node, graph, querySequence):
  return len(node.attributes)

# Feature: the average E-Value
def featAvgEValue(predictor, node, graph, querySequence):
  cAttrs, sumAttrEVal = len(node.attributes), 0.0
  for hit, attr in node.attributes.iteritems():
    sumAttrEVal += attr[ "hit_value" ]
  return sumAttrEVal / cAttrs

# Feature: the average E-Value
def featProdEValue(predictor, node, graph, querySequence):
  prodAttrEVal = 1.0
  for hit, attr in node.attributes.iteritems():
    sumAttrEVal *= attr[ "hit_value" ]
  return sumAttrEVal

# Feature: The best hit length
def featMaxEValueHitLength(predictor, node, graph, querySequence):
  maxEVal, maxHitLength = None, 0
  for hit, attr in node.attributes.iteritems():
    attrEVal = attr[ "hit_value" ]
    attrHitLength = attr[ "hit_to" ] + 1 - attr[ "hit_from" ]
    if maxEVal == None:
      maxEVal, maxHitLength = attrEVal, attrHitLength
    elif maxEVal < attrEVal:
      maxEVal, maxHitLength = attrEVal, attrHitLength
  return maxHitLength

# Feature: The longest hit length
def featLongestHitLength(predictor, node, graph, querySequence):
  longestHitLength = 0
  for hit, attr in node.attributes.iteritems():
    attrHitLength = attr[ "hit_to" ] + 1 - attr[ "hit_from" ]
    longestHitLength = max(longestHitLength, attrHitLength)
  return longestHitLength

# Feature: average hit length
def featAverageHitLength(predictor, node, graph, querySequence):
  sum, nr = 0, len(node.attributes)
  for hit, attr in node.attributes.iteritems():
    sum += attr[ "hit_to" ] + 1 - attr[ "hit_from" ]
  return sum / nr

# Feature: 
#def feat(predictor, node, graph, querySequence):
#  pass

# some helper functions, for the feature functions
def getSequenceByHitId(id):
#  [ "hit_id" ]
  pass
