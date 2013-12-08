#! /usr/bin/env python

# ok, this is a file containing all features that will be used by the predictor.py to predict if the hpo term is correct for this sequence or not
# note, that all feature functions starts with feat

# Feature: the best node method
def featBestHitMethod(predictor, node, graph, querySequence):
  minEVal, method = None, None
  for hit, attr in node.attributes.iteritems():
    attrEVal = attr[ "hit_value" ]
    if minEVal == None:
      minEVal = attrEVal
      method = attr[ "method" ]
    elif attrEVal < minEVal:
      minEVal = attrEVal
      method = attr[ "method" ]
  if method == None:
    return 0
  if method == "blast":
    return 1
  return -1

# Feature: node graph position
def featNodePositionMin(predictor, node, graph, querySequence):
  if hasattr(node, "is_a"):
    if type(node.is_a) == type([]):
      height = 9999999999999
      for n in node.is_a:
        height = min(height, featNodePositionMin(predictor, n, graph, querySequence))
      return 1 + height
    else:
      return 1 + featNodePositionMin(predictor, node.is_a, graph, querySequence)
  else:
    return 1

# Feature: node graph position
def featNodePositionMax(predictor, node, graph, querySequence):
  if hasattr(node, "is_a"):
    if type(node.is_a) == type([]):
      height = 9999999999999
      for n in node.is_a:
        height = max(height, featNodePositionMin(predictor, n, graph, querySequence))
      return 1 + height
    else:
      return 1 + featNodePositionMin(predictor, node.is_a, graph, querySequence)
  else:
    return 1

# Feature: The sequence length of the query
def featQuerySequenceLength(predictor, node, graph, querySequence):
  return len(querySequence)

# Feature: the coverage of the query sequence to all hit sequences
def featLengthCoverage(predictor, node, graph, querySequence):
  cov = []
  for i in querySequence:
    cov.append( False )
  for hit, attr in node.attributes.iteritems():
    for i in range(attr[ "hit_from" ] - 1, attr[ "hit_to" ]):
      i = True
  l = 0
  for i in cov:
    if i:
      l += 1
  return l * 100.0 / len(querySequence)

# Feature: return the best E-Value of all sequences
def featMinEValue(predictor, node, graph, querySequence):
  minEVal = None
  for hit, attr in node.attributes.iteritems():
    attrEVal = attr[ "hit_value" ]
    if minEVal == None:
      minEVal = attrEVal
    else:
      minEVal = min(minEVal, attrEVal)
  return minEVal

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
  sumAttrEVal = 1.0
  for hit, attr in node.attributes.iteritems():
    sumAttrEVal *= attr[ "hit_value" ]
  return sumAttrEVal

# Feature: The best hit length
def featMinEValueHitLength(predictor, node, graph, querySequence):
  minEVal, minHitLength = None, 0
  for hit, attr in node.attributes.iteritems():
    attrEVal = attr[ "hit_value" ]
    attrHitLength = attr[ "hit_to" ] + 1 - attr[ "hit_from" ]
    if minEVal == None:
      minEVal, minHitLength = attrEVal, attrHitLength
    elif minEVal > attrEVal:
      minEVal, maxHitLength = attrEVal, attrHitLength
  return minHitLength

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

# Feature: number of nodes on the same level
#def featNodeSamelvl(predictor, node, graph, querySequence):
#  parents = graph.getParents(node)
#  childs = []
#  for p in parents:
#    childs.extend(graph.getChildrens(p))
#  return len(list(set(childs)))

# Feature: 
#def feat(predictor, node, graph, querySequence):
#  pass

# some helper functions, for the feature functions
def getSequenceByHitId(id):
#  [ "hit_id" ]
  pass
