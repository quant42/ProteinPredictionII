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
        for line in lines:
          # do nothing, if HpoTerm is_obsolete
          if line.startswith('is_obsolete:'):
            return
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
  
  def getHpoSubGraph(self, idLst, addAttr = None):
    
    """ build a hpo sub tree containing only the id in the idList and their parents """
    
    # create a new Hpo(Sub)Graph to return
    ret = HpoGraph( None )
    # ok, put in the stuff in
    for id in idLst:
      term = self.getHpoTermById( id )
      while hasattr(term, "is_a"):
        # add an attribute to the term?
        if addAttr != None:
          term.attributes.update( addAttr )
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
      # add an attribute to the term?
      if addAttr != None:
        term.attributes.update( addAttr )
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
  
  def getLeaves(self):
    
    """ return a list with the ids of all leaves of the graph  """
    
    # create the list to return
    result = []
    # add all objects, that have leads available in the graph
    for key in self.hpoTermsDict:
      # check, if all children are not in the graph
      all = True
      for child in self.hpoTermsDict[key].childrens:
        if child in self:
          all = False
          break
      if all:
        result.append( key )
    # return this
    return result
  
  def getChildrens(self, node):
    
    """ check each children, if they are in the graph """
    
    if isinstance(node, str):
      node = self.getHpoTermById( node )
    lst = []
    for c in node.childrens:
      if c in self:
        lst.append( c )
    return lst
  
  def getParents(self, node):
    
    """ check each parent, if they are in the graph """
    
    if isinstance(node, str):
      node = self.getHpoTermById( node )
    lst = []
    if hasattr(node, "is_a"):
      if isinstance(node.is_a, list):
        for c in node.is_a:
          if c in self:
            lst.append( c.split(" ")[0] )
      else:
        if node.is_a in self:
          lst.append( node.is_a.split(" ")[0] )
    return lst
  
  def getRoot(self, multiRootLog = True):
    
    """ returns the root of this graph, write a log if there're more than one root """
    
    # create the list to return
    result = []
    # add all objects, that have don't have an is_a relation chip or which parents are not available in the graph
    for key in self.hpoTermsDict:
      # check, if parent is not in graph
      if self.getParents( key ) == []:
        result.append( key )
    # check log
    if multiRootLog and len(result) != 1:
      out.writeWarning("WARNING: found unexpected multiple (or none) roots in graph!")
    # return this
    print "root: " + str(result)
    return result
  
  def writeSvgImage(self, fileName = "graph.svg", addAttrs = False, xGap = 200, yGap = 120, circleR = 5, circleFill = "red", circleStroke = "black", circleStrokeWidth = 1, lineColor = "black", lineWidth = 2, textColor = "green"):
    
    """ create an svg image of this graph for better discussions """
    
    # helper functions
    def getCircleCode(x, y, r, stroke, strokeWidth, fill):
      return "<circle cx=\"{}\" cy=\"{}\" r=\"{}\" stroke=\"{}\" stroke-width=\"{}\" fill=\"{}\" />\n".format( x + 20, y + 20, r, stroke, strokeWidth, fill )
    def getLineCode(x1, y1, x2, y2, lineColor, lineWidth):
      return "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" style=\"stroke: {}; stroke-width: {}\" />\n".format( x1 + 20, y1 + 20, x2 + 20, y2 + 20, lineColor, lineWidth )
    def getStrCode(x, y, id, attr, attrAppend, color):
      text = "<text x=\"{}\" y=\"{}\" fill=\"{}\" style=\"font-size: 18px\">{}</text>\n".format( x + 30, y + 20, color, id, attr )
      if attrAppend:
        text += "<text x=\"{}\" y=\"{}\" fill=\"{}\" style=\"font-size: 16px\">{}</text>\n".format( x + 35, y + 45, color, attr )
      return text
    def calcNodePos(lst, node, w, h, wE, hE):
      i, j, k = -1, -1, -1
      for l in lst:
        i += 1
        try:
          j = l.index(node)
          k = len( l )
          break
        except ValueError:
          pass
      return [ j * w / k + (w / k - wE) / 2, i * hE ]
    # calculate the level of all nodes
    lvl = [ self.getRoot( multiRootLog = False ) ]
    def extendLvls(self, lvl):
      nextLvl = []
      for cLvlNode in lvl[-1:][0]:
        for child in self.getChildrens( cLvlNode ):
          if len( self.getParents( child ) ) <= 1:
            nextLvl.extend( [ child ] )
          else:
            # ok, multiroot, this makes it more difficult
            appended = self.getParents( child )
            stop = False
            for l in lvl:
              for c in l:
                if c == cLvlNode:
                  stop = True
                  break
                try:
                  appended.remove( c )
                except ValueError:
                  pass
              if stop:
                break
            if len( appended ) <= 1:
              nextLvl.extend( [ child ] )
      lvl.extend( [ nextLvl ] )
      return len( nextLvl ) != 0
    while extendLvls(self, lvl):
      pass
    lvl = lvl[:-1]
    # get some data
    maxV = 0
    for l in lvl:
      maxV = max( maxV, len( l ) )
    w, h = xGap * maxV, yGap * len( lvl )
    # now write that (header) to the file
    f = open (fileName, "w+")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" baseProfile=\"full\" width=\"{}px\" height=\"{}px\" viewBox=\"0 0 {} {}\">\n".format( w, h, w, h ) )
    # first lines
    for l in lvl[1:]:
      for n in l:
        n1 = calcNodePos(lvl, n, w, h, xGap, yGap)
        for p in self.getParents( n ):
          n2 = calcNodePos(lvl, p, w, h, xGap, yGap)
          f.write( getLineCode(n1[0], n1[1], n2[0], n2[1], lineColor, lineWidth ) )
    # second text
    for l in lvl:
      for n in l:
        n1 = calcNodePos(lvl, n, w, h, xGap, yGap)
        n_ = self.getHpoTermById( n )
        f.write( getStrCode(n1[0], n1[1], n_.id, n_.attributes, addAttrs, textColor) )
    # last points
    for l in lvl:
      for n in l:
        n1 = calcNodePos(lvl, n, w, h, xGap, yGap)
        f.write( getCircleCode(n1[0], n1[1], circleR, circleStroke, circleStrokeWidth, circleFill) )
    # svg eof
    f.write("</svg>\n")
    f.close()
  
class HpoTerm():
  
  """ This is a class representing a single hpoterm """
  
  def __init__(self, hpoTermLines):
    
    """ This initalize a hpoterm by the lines of an [Term] in an hpo file """
    
    # add an array for the childrens
    self.childrens = []
    self.attributes = {}
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
  print "HP:0000008" in graph.getLeaves()
#  print dir(graph.getHpoTermById("HP:0000008"))
#  print graph.getHpoTermById("HP:0000008").is_a
#  print len(graph.hpoTermsDict)
  sub1 = graph.getHpoSubGraph(["HP:0000008"])
  sub2 = graph.getHpoSubGraph(["HP:0000119"])
#  print(sub1.hpoTermsDict)
#  print(sub2.hpoTermsDict)
#  g = (sub1 - sub2)
#  print g.getRoot()
#  print g.hpoTermsDict
  graph.writeSvgImage()
#  print("HP:0000008" in sub1)
