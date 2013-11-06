#! /usr/bin/env python

# ===================================================================
# This class provides functions for searching for simmilar proteins
# with the blast algorithm. Therefor blast must be installed locally
# (Ubuntu: sudo apt-get install blast2) or the ncbi blast must be
# available.
# Call Blast.ncbiBlast(seq="") or Blast.localBlast(seq="", 
# database="") to do the blast alignments. You will get a Blast class
# which has an attribute alignments.
# ===================================================================

import out, commands, re

class Blast():
  
  """ A basic blasting class """
  
  # constructor for building this class, if the header of the sequences, the sequences them self and the
  # corresponding blastResults are already known
  def __init__(self, blastResults):
    out.writeDebug("Initalize Blast Alignment by blasting results ...")
    self.rawResults = blastResults
    # self stuff
    self.alignments = []
    # parse the blast results
    beginOfResults = False
    lines = blastResults.split('\n')
    tmp = []
    for line in lines:
      # skip empty lines
      if not line.strip():
        continue
      # skip all lines about the authors, blast improvments etc. until the actual searching results begin
      if beginOfResults:
        if line[0] == ">":
          self.__analyseTmp(tmp)
          tmp = []
        elif line.startswith("  Database: "):
          self.__analyseTmp(tmp)
          tmp = []
        tmp.append( line )
      else:
        if line.find("Sequences producing significant alignments:") != -1 or line.find("***** No hits found ******") != -1:
          beginOfResults = True
    self.__analyseEnd(tmp)
  
  def __analyseTmp(self, tmp):
    # skip empty analysings
    if len(tmp) == 0:
      return
    # ok check type, is the first with >
    if tmp[0][0] != ">":
      out.writeDebug("\n".join(tmp))
    else:
      # ok, this is a list with all found 
      out.writeLog("\n".join(tmp))
  
  def __analyseEnd(self, tmp):
    vars = \
    [
      "  Database: ", "    Posted date: ", "  Number of letters in database: ",
      "  Number of sequences in database:  ", "Matrix: ", "Number of Sequences: ",
      "Number of Hits to DB: ", "Number of extensions: ", "Number of successful extensions: ",
      "Number of sequences better than 10.0: ", "Number of HSP's gapped: ",
      "Number of HSP's successfully gapped: ", "Length of query: "
    ]
    for line in tmp:
      if line.startswith("  Database: "):
        self.database = line[12:]
      elif self.startswith("    Posted date: "):
        self.date = line[17:].strip()
      elif self.startswith("  Number of letters in database: "):
        slef.dbLetterSize = line[:].strip()
  
  @staticmethod
  def ncbiBlast(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP"):  # TODO
    # well do a protein blast search with ncbi
    output.writeDebug("Init a blastp ncbi search ...")
    import ncbi
    # todo aquire a lock, so that by multithreading only one request every two seconds will be send
    request = sendNcbiBlastRequest( sequence )
    time.sleep(float(request[1]))
  
  @staticmethod
  def localBlast(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP", database = "../data/genes_UniProt.fasta"):
    out.writeDebug( "Do a local blast search for {} in {}".format( seq, database ) )
    blastResults = commands.getstatusoutput( "echo \"%s\" | blast2 -m 7 -p blastp -d ../data/genes_UniProt.fasta" % seq )
    if blastResults[0] != 0:
      out.writeLog("Return code for blast search {} in {} returned with exit code {}!".format( seq, database, blastResults[0] ) )
    return  blastResults[1] 

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  b = Blast.localBlast(seq = "WPVIIFIILAIT") #"PPFKTRTIALIIFIIVPW")
  print b
