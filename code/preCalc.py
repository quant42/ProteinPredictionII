#! /usr/bin/env python

# This does a precalculation for blast and hhblits

import blast, hhblits

blastDB = "../data/genes_UniProt.fasta"
hhDB = "../data/PP2db"
out = "../data/lookup0.dat"
fastaFile = "../data/dataset_0.fa"

def predictSequence(file, id, seq, dbBlast, dbHHB, minEValBlast = 0.1):
  print("Do record: " + str(record.id))
  g.write("{}\n".format(id))
  blastResults = blast.Blast.localBlast(seq=seq, database=dbBlast, minEVal=minEValBlast)
  for hit in blastResults.hits:
    g.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(hit["method"], hit["hit_id"], hit["hit_value"], hit["hit_from"], hit["hit_to"], hit["hit_order"]))
  hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=seq, database=dbHHB)
  for hit in hhblitsResults.hits:
    g.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(hit["method"], hit["hit_id"], hit["hit_value"], hit["hit_from"], hit["hit_to"], hit["hit_order"]))

from Bio import SeqIO

g = open(out, "w+")
f = open(fastaFile, "rU")
for record in SeqIO.parse(f, "fasta"):
  predictSequence(g, record.id, str(record.seq), blastDB, hhDB)
f.close()
g.close()
