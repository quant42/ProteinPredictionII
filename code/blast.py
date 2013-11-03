#! /usr/bin/env python

# ===================================================================
# This class provides functions for searching for simmilar proteins
# with the blast algorithm. Therefor blast must be installed locally
# (Ubuntu: sudo apt-get install blast2) or the ncbi blast must be
# available.
# 
# 
# ===================================================================

import socket, time

class Blast():
  
  """ A basic blasting class """
  
  # a timestamp for blasting with ncbi
  
  # constructor for building this class, if the header of the sequences, the sequences them self and the
  # corresponding blastResults are already known
  def __init__(self, header, sequences, blastResults):
    pass
  
  @staticmethod
  def ncbiBlast(sequence):
    pass
  
  @staticmethod
  def localBlast(header = None, seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP", database = "../data/genes_UniProt.fasta"):
    
    return 

def blast(seq):
  print "blast seq %s" % seq
  import commands
  blastResult = commands.getstatusoutput("echo \"%s\" | blast2 -p blastp -d ../data/genes_UniProt.fasta" % seq)
  return Blast

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  print(blast(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP"))
