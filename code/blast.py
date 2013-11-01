#! /usr/bin/env python

# This is some example code to run a blast search

def blast(seq):
  print "blast seq %s" % seq
  import commands
  return commands.getstatusoutput("echo \"%s\" | blast2 -p blastp -d ../data/genes_UniProt.fasta" % seq)


if __name__ == "__main__":
  print(blast("NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP"))
