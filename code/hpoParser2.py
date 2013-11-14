#! /usr/bin/env python

import out

class HpoGraph():
  
  """ A representation of the a hpo graph """
  
  def __init__(self, hpoFile="../data/hp.obo"):
    
    """ initalize an hpo graph by an hpo file """
    
    # debug message
    out.writeDebug( "parsing hpo file " + str( hpoFile ) )
    # init main class varibale
    self.hpoTermsDict = {}
    self.roots = []
    # if the file to parse is None, an empty HpoGraph will be returned
    if hpoFile == None:
      return
    # ok, parse the lines in the file
    try:
      node_id = ''
      for line in open(hpoFile):
        if line.startswith('id:'):
          node_id = line.split()[-1]
          self.hpoTermsDict[node_id] = HpoTerm(node_id)
        elif line.startswith('is_obsolete:'):
          del self.hpoTermsDict[node_id]
      for line in open(hpoFile):
        if line.startswith('id:'):
          node_id = line.split()[-1]
        elif line.startswith('is_a:') and node_id in self.hpoTermsDict:
          parentnode = line.split()[1]
          self.hpoTermsDict[node_id].parent_nodes.append(parentnode)
          self.hpoTermsDict[parentnode].child_nodes.append(node_id)
      for node_id, node in self.hpoTermsDict.iteritems():
        if not node.parent_nodes:
          self.roots.append(node_id)

    except Exception as e:
      out.writeError("Error parsing hpo file " + str( e.message ) + " " + str( e.args) )
  
  def getHpoTermById(self, id):
    
    """ returns an hpo term by an hpo id """
    
    try:
      return self.hpoTermsDict[id.split(" ")[0]]
    except KeyError:
      return None
  
  def getHpoSubGraph(self, idLst):
    
    """ build a hpo sub tree containing only the id in the idList and their parents """
    
    # create a new Hpo(Sub)Graph to return
    ret = HpoGraph(None)
    def add_nodes(id_list):
      for node_id in id_list:
        ret.hpoTermsDict.update( { node_id : self.getHpoTermById( node_id ) } )
        if ret.hpoTermsDict[node_id].parent_nodes:
          add_nodes(ret.hpoTermsDict[node_id].parent_nodes)
        elif node_id not in ret.roots:
          ret.roots.append(node_id)

    # ok, put in the stuff in
    add_nodes(idLst)
        
    # return subgraph
    return ret
  
  def __add__(self, other):
    pass
  def __sub__(self, other):
    pass

class HpoTerm():
  
  """ This is a class representing a single hpoterm """
  
  def __init__(self, id):
    """ This initalizes an hpo term with hpo id"""
    self.id = id
    self.child_nodes = []
    self.parent_nodes = []
    self.visited = 0
    

if __name__ == "__main__":
  graph = HpoGraph()
  print dir(graph)
  print dir(graph.getHpoTermById("HP:0000008"))
  print graph.getHpoTermById("HP:0000008").parent_nodes
  print len(graph.hpoTermsDict)
  print graph.getHpoSubGraph(["HP:0000008"]).roots
