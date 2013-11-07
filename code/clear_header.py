import re


for line in open('/home/jonathan/Uni/PP2/ProteinPredictionII/data/genes_UniProt.fasta'):
    if line.startswith('>'):
        print '>'+line.split('|')[1]
    else:
        print line,
