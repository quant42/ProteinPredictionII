#! /usr/bin/env python

# this is the predictor function, that runs the prediction for a graph
	
# imports
import pickle, features, out
from random import shuffle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


# some const
ACCEPTED = 1
NOTACCEPTED = -1

class Predictor():
  
  """ The predictor for a node """
  
  def __init__(self, netFile):
    
    """ Initalize a predictor from with a neuronal network. If the neuronalNetFile is None, an "empty" predictor to train is returned! """
    
    # init the features
    self.features = []
    functions = dir(features)
    for function in functions:
      if function.startswith('feat'):
        self.features.append(getattr(features,function))
    
    # init the network
    if netFile:
      # ok, load the predictor
      f = open(netFile,'r')
      self.net = pickle.load(f)
      f.close()
    else:
      # create an empty predictor
      cFeatures = len(self.features)
      self.net = buildNetwork( cFeatures, cFeatures + 1, 3, 1)
  
  def runprediction(self, querySequence, graph):
    
    """ this function marks all nodes in the graph as accepted, if the prediction they are predicted to be positive, Note, that node.accpeted should be false for all nodes.
    This function set the node.accpeted = True, for all nodes that are accepted by the predictor. """
    
    def acceptNodeAndParentNodes(graph, node):
      node.accepted = True
      stack = graph.getParents(node)
      while len(stack) != 0:
        cNode = graph.getHpoTermById(stack.pop())
        cNode.accepted = True
        stack.extend(graph.getParents(cNode))
    
    toPredict = graph.getLeaves()
    
    while len(toPredict) != 0:
      # ok, get the node to predict
      cNode = graph.getHpoTermById(toPredict[0])
      toPredict = toPredict[1:]
      # do next, if node was already accepted (by a child node)
      if cNode.accepted:
        continue
      # get all features for the current node
      featuresValue = []
      for feature in self.features:
        featuresValue.append(feature(self, cNode, graph, querySequence))
      # ok, now run the neuronal network
      predictionResult = self.net.activate(featuresValue)
      out.writeLog("Prediction result for node {} = {}".format(cNode.id, predictionResult))
      # check the prediction result
      if predictionResult[0] > (ACCEPTED + NOTACCEPTED) / 2:
        # ok, the node was accepted, by the neuronal network, so set accepted
        acceptNodeAndParentNodes(graph, cNode)
      else:
        # check parents if maybe they will be accepted
        toPredict.extend(graph.getParents(cNode))
  
  def trainprediction(self, data=None, biased=True):
    if not data:
      out.writeDebug('No training data! The net stays initialized with random weights!')
      print 'no data'
      return False

    #create supervised data set from the training nodes
    ds = SupervisedDataSet(len(self.features), 1)
    reduced_dataset = set([])
    for node, target in data:
      featuresValue = []
      for feature in self.features:
        featuresValue.append(feature(self, node, None, ''))
      # TODO: check instances for redundancy (parent nodes look probably similar..)
      # remove bias in the instances
      if target:
        reduced_dataset.add(tuple(featuresValue+[ACCEPTED]))        
      else:
        reduced_dataset.add(tuple(featuresValue+[NOTACCEPTED]))

    for instance in reduced_dataset:
      ds.addSample(instance[:-1],instance[-1])
      
    trainer = BackpropTrainer(self.net, ds)
    trainer.trainUntilConvergence()
    
    return True      
  
  def saveNeuronalNetwork(self, fileName):
    
    """ save the neuronal network to a file """
    
    fileObj = open(fileName, "w+")
    pickle.dump(net, fileObj)
    fileObj.close()

if __name__ == "__main__":
  pass
