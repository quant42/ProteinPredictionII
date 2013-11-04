#! /usr/bin/env python

# ===================================================================
# This class provides functions for searching for simmilar proteins
# with the blast algorithm. Therefor blast must be installed locally
# (Ubuntu: sudo apt-get install blast2) or the ncbi blast must be
# available.
# 
# 
# ===================================================================

import out, commands

class Blast():
  
  """ A basic blasting class """
  
  # a timestamp for blasting with ncbi
  
  # constructor for building this class, if the header of the sequences, the sequences them self and the
  # corresponding blastResults are already known
  def __init__(self, blastResults):
    # parse the blast results
    beginOfResults = False
    lines = blastResults.split('\n')
    result = ""
    for line in lines:
      # skip empty lines
      if not line.strip():
        continue
      # skip all lines about the authors, blast improvments etc. until the actual searching results begin
      if beginOfResults:
        result += line + "\n"
      else:
        if line.find("Sequences producing significant alignments:") != -1:
          beginOfResults = True
    out.writeLog(result)
  
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
    blastResults = commands.getstatusoutput( "echo \"%s\" | blast2 -p blastp -d ../data/genes_UniProt.fasta" % seq )
    if blastResults[0] != 0:
      out.writeLog("Return code for blast search {} in {} returned with exit code {}!".format( seq, database, blastResults[0] ) )
    return Blast( blastResults[1] )

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  Blast.localBlast()
