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
        self.hpoTermsDict.update( { term.id : term } )
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
    # ok, put in the stuff in
    for id in idLst:
      self.hpoTermsDict.update( { id : self.getHpoTermById( id ) } )
    # return subgraph
    return ret
  
  def __add__(self, other):
    pass
  def __sub__(self, other):
    pass

class HpoTerm():
  
  """ This is a class representing a single hpoterm """
  
  def __init__(self, hpoTermLines):
    
    """ This initalize a hpoterm by the lines of an [Term] in an hpo file """
    
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
  print dir(graph)
  print dir(graph.getHpoTermById("HP:0000008"))
  print graph.getHpoTermById("HP:0000008").is_a
  print len(graph.hpoTermsDict)
