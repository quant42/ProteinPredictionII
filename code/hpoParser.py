#! /usr/bin/env python

import out

class HpoGraph():
  
  """ A representation of the a hpo graph """
  
  def __init__(self, hpoFile="../data/hp.obo"):
    
    """ initalize an hpo graph by an hpo file """
    
    # debug message
    if hpoFile != None:
      out.writeDebug( "parsing hpo file " + str( hpoFile ) )
    else:
      out.writeDebug( "creating new subgraph!" )
    # init main class varibale
    self.hpoTermsDict = {}
    self.isSubTree = hpoFile == None
    # if the file to parse is None, an empty HpoGraph will be returned
    if hpoFile == None:
      return
    # helper function to analyse the lines
    def _analyseLines(self, lines):
      
      """ Analyse the parsed lines (helper function) """
      
      # file descriptor or hp term?
      if lines[0].startswith( "[Term]" ):
        # add a hpoterm by the hpoterms description
        term = HpoTerm( lines[1:] )
        self.hpoTermsDict.update( { term.id.split(" ")[0] : term } )
      else:
        for line in lines:
          # ok, get the position of the :
          attrName = line[:line.find(":")].strip()
          attrVal = line[line.find(":")+1:].strip()
          # now add this as attribute
          if hasattr(self, attrName):
            if isinstance(getattr(self, attrName), list):
              getattr(self, attrName).append( attrVal )
            else:
              setattr(self, attrName, [ getattr(self, attrName), attrVal ])
          else:
            setattr(self, attrName, attrVal)
    # ok, parse the lines in the file
    try:
      f = file( hpoFile, "r" )
      lines = []
      for line in f:
        # skip empty lines
        if line.strip() == "":
          continue
        # do something for non empty lines
        if line.startswith( "[Term]" ):
          _analyseLines(self, lines)
          lines = [ line ]
        else:
          lines.append(line)
      _analyseLines(self, lines)
      f.close()
    except Exception as e:
      out.writeError("Error parsing hpo file " + str( e.message ) + " " + str( e.args) )
    # good and now create the relation ship childrens
    for key in self.hpoTermsDict:
      node = self.hpoTermsDict[key]
      if hasattr(node, "is_a"):
        if isinstance(node.is_a, list):
          for element in node.is_a:
            self.hpoTermsDict[ element.split(" ")[0] ].childrens.append(key)
        else:
          self.hpoTermsDict[ node.is_a.split(" ")[0] ].childrens.append(key)
  
  def __contains__(self, key):
    # if key is string check, if key is a key for an object
    if isinstance( key, str ):
      return self.getHpoTermById( key, log = False ) != None
    # if key is object, check if key is located in dict
    else:
      for iterKey in self.hpoTermsDict:
        if self.hpoTermsDict( iterKey ) == key:
          return True
      return False
  
  def getHpoTermById(self, id, log = True):
    
    """ returns an hpo term by an hpo id """
    
    try:
      return self.hpoTermsDict[id.split(" ")[0]]
    except KeyError:
      if log:
        out.writeLog( "KeyError getting term for id: \"" + str( id ) + "\"! => returning None!" )
      return None
  
  def getHpoSubGraph(self, idLst):
    
    """ build a hpo sub tree containing only the id in the idList and their parents """
    
    # create a new Hpo(Sub)Graph to return
    ret = HpoGraph( None )
    # ok, put in the stuff in
    for id in idLst:
      term = self.getHpoTermById( id )
      while hasattr(term, "is_a"):
        # save previous
        ret.hpoTermsDict.update( { term.id.split(" ")[0] : term } )
        # load next
        if isinstance( term.is_a, list ):
          # ok, there're more than one is_a attrs, so add both
          restLst = term.is_a[1:]
          term = self.getHpoTermById( term.is_a[0] )
          idLst.extend( restLst )
        else:
          term = self.getHpoTermById( term.is_a )
        # exit, if key already exists (even cylclic graphs don't matters then)
        if ret.hpoTermsDict.has_key( term.id ):
          break
      # add root
      ret.hpoTermsDict.update( { term.id.split(" ")[0] : term } )
    # return subgraph
    return ret
  
  def __add__(self, other):
    
    """ returns a subgraph that contains both nodes """

    # create a new Hpo(Sub)Graph to return    
    ret = HpoGraph( None )
    dict = {}
    dict.update(self.hpoTermsDict)
    dict.update(other.hpoTermsDict)
    ret.hpoTermsDict = dict
    # return subgraph
    return ret
  
  def __sub__(self, other):
    
    """ returns a subgraph that contains only those nodes availabe in both subgraphs """
    
    # create a new Hpo(Sub)Graph to return
    ret = HpoGraph( None )
    dict = {}
    for key in self.hpoTermsDict.iterkeys():
      if other.hpoTermsDict.has_key( key ):
        dict.update( { key : self.hpoTermsDict[key] } )
    ret.hpoTermsDict = dict
    # return subgraph
    return ret
  
  def getLeafs(self):
    
    """ return a list with the ids of all leaves of the graph  """
    
    # create the list to return
    result = []
    # remove all objects, that have leads available in the graph
    for key in self.hpoTermsDict:
      # check, if all children are not in the graph
      all = True
      for child in self.hpoTermsDict[key].childrens:
        if child in self.hpoTermsDict:
          all = False
          break
      if all:
        result.append( key )
    # return this
    return result
  
  def getChildrens(self, node):
    
    """ check each children, if they are in the graph """
    
    lst = []
    for c in node.childrens:
      if c in self:
        lst.append( c )
    return lst
  
class HpoTerm():
  
  """ This is a class representing a single hpoterm """
  
  def __init__(self, hpoTermLines):
    
    """ This initalize a hpoterm by the lines of an [Term] in an hpo file """
    
    # add an array for the childrens
    self.childrens = []
    # ok, parse the rest of the lines
    for line in hpoTermLines:
      # ok, thats a good line with a good description
      # parse for :
      attrName = line[:line.find(":")].strip()
      attrVal = line[line.find(":")+1:].strip()
      # ok, now append this attr
      if hasattr(self, attrName):
        if isinstance(getattr(self, attrName), list):
          getattr(self, attrName).append( attrVal )
        else:
          setattr(self, attrName, [ getattr(self, attrName), attrVal ])
      else:
        setattr(self, attrName, attrVal)

if __name__ == "__main__":
  graph = HpoGraph()
  print "HP:0000008" in graph.getLeafs()
#  print dir(graph.getHpoTermById("HP:0000008"))
#  print graph.getHpoTermById("HP:0000008").is_a
#  print len(graph.hpoTermsDict)
  sub1 = graph.getHpoSubGraph(["HP:0000008"])
  sub2 = graph.getHpoSubGraph(["HP:0000119"])
#  print(sub1.hpoTermsDict)
#  print(sub2.hpoTermsDict)
  print((sub1 - sub2).getLeafs())
#  print("HP:0000008" in sub1)
