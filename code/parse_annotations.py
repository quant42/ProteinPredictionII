#!/usr/bin/env python
from collections import defaultdict
from re import sub
seq_file = '/home/jonathan/Uni/PP2/ProteinPredictionII/data/genes_UniProt.fasta'
ann_file = '/home/jonathan/Uni/PP2/ProteinPredictionII/data/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'


seq_to_annotation = {}
seq_to_gene_name = {}
gene_name_to_sequence = defaultdict(list)
seqs_wo_gene_name = []
seq_list = []
seq_set = set([])
for line in open(seq_file):
    if line.startswith('>'):
        items = line.split()
        seq_id = sub('>','',items[0])
        name_found = False
        seq_list.append(seq_id)
        seq_set.add(seq_id)
        seq_gene_name = ''
        for item in items[1:]:
            if item.startswith('GN'):
                name_found = True
                seq_gene_name = item.split('=')[1]
        if not name_found:
            seqs_wo_gene_name.append(seq_id)
        else:
            #if seq_id in seq_to_gene_name:
                #print 'redundant:',seq_id
                #print 'old gene name:',seq_to_gene_name[seq_id]
                #print 'new gene name:',seq_gene_name
            seq_to_gene_name[seq_id] = seq_gene_name
            seq_to_annotation[seq_id] = []
            gene_name_to_sequence[seq_gene_name].append(seq_id)

#print "parsed %s sequences, %s are uniqe, %s have a gene name"%(len(seq_list), len(seq_set), len(seq_to_gene_name))
if len(seqs_wo_gene_name) != 0:
    print 'missing gene names, parsing will be incomplete'

for line in open(ann_file):
    items = line.split()[1:]
    gene_name = items[0]
    HPO_annotation = items[-1]
    for seq_id in gene_name_to_sequence[gene_name]:
        seq_to_annotation[seq_id].append(HPO_annotation)

annotated_sequences = 0
for seq, annotations in seq_to_annotation.iteritems():
    if len(annotations) == 0:
        continue
        print 'no annotations for %s' %seq
    else:
        print "%s\t%s"%(seq, ','.join(annotations))
        annotated_sequences += 1
#print '%s sequences, %s have no annotations' %(len(seq_to_annotation),
#                                             len(seq_to_annotation) - annotated_sequences)
            
    
