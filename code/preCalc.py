#! /usr/bin/env python

# This does a precalculation for blast and hhblits

import blast, hhblits
import sys

blastDB = "../data/genes_UniProt.fasta"
hhDB = "../data/PP2db"
out = "../data/lookup{}.dat".format(sys.argv[1])
fastaFile = "../data/dataset_{}.fa".format(sys.argv[1])

def predictSequence(file, id, seq, dbBlast, dbHHB, minEValBlast = 0.1):
  g.write("{}\n".format(id))
  blastResults = blast.Blast.localBlast(seq=seq, database=dbBlast, minEVal=minEValBlast)
  for hit in blastResults.hits:
    g.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(hit["method"], hit["hit_id"], hit["hit_value"], hit["hit_from"], hit["hit_to"], hit["hit_order"]))
  hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=seq, database=dbHHB)
  for hit in hhblitsResults.hits:
    g.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(hit["method"], hit["hit_id"], hit["hit_value"], hit["hit_from"], hit["hit_to"], hit["hit_order"]))

from Bio import SeqIO
#from os import listdir

g = open(out, "w+")
f = open(fastaFile, "rU")
for record in SeqIO.parse(f, "fasta"):
  predictSequence(g, record.id, str(record.seq), blastDB, hhDB)
  g.flush()
f.close()
g.close()
