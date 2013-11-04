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
    out.writeLog(blastResults)
  
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
    out.writeDebug("Do a local blast search for %s in %s" % (seq, database))
    blastResults = Blast( commands.getstatusoutput( "echo \"%s\" | blast2 -p blastp -d ../data/genes_UniProt.fasta" % seq ) )
    return Blast( blastResults )

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  Blast.localBlast()
