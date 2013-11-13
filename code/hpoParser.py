#! /usr/bin/env python

import out

class HpoGraph():
  
  """ A representation of the a hpo graph """
  
  def __init__(self, hpoFile="../data/hp.obo"):
    
    """ initalize an hpo graph by an hpo file """
    
    # init main class varibale
    self.hpoTerms = []
    self.hpoGraph = {}
    # helper function to analyse the lines
    def _analyseLines(self, lines):
      
      """ Analyse the parsed lines (helper function) """
      
      # file descriptor or hp term?
      if lines[0].startswith( "[Term]" ):
        # add a hpoterm by the hpoterms description
        self.hpoTerms.append( HpoTerm( lines ) )
      else:
        for line in lines:
          if line.strip() != "":
            # ok, get the position of the :
            attrName = line[:line.find(":")].strip()
            attrVal = line[line.find(":")+1:].strip()
            # now add this as attribute
            print attrName + ": " + attrVal
    
    # ok, parse the lines in the file
    try:
      f = file( hpoFile, "r" )
      lines = []
      for line in lines:
        if line.startswith( "[Term]" ):
          _analyseLines(self, lines)
          lines = [ line ]
        else:
          lines.append(line)
      _analyseLines(self, lines)
      f.close()
    except Exception as e:
      out.writeError("Error parsing hpo file " + str( e.message ) + " " + str( e.args) )
  
  def getSubGraph(self):
    pass

class HpoTerm():
  
  """ This is a class representing a single hpoterm """
  
  def __init__(self, hpoTermStr):
    pass

if __name__ == "__main__":
  graph = HpoGraph()
