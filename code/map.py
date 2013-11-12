from collections import defaultdict

fasta_file = '../data/genes_UniProt.fasta'
annotation_file = '../data/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
mapping_file = '../data/automatic_mapping'
mapping_Uniprot_Entrez = defaultdict(list) 

uniprot = {}

for line in open(fasta_file):
    if line.startswith('>'):
        uniprot[line.strip()[1:]] = True

entrez = defaultdict(list) 

for line in open(annotation_file):
    tmp = line.split()
    gene_id = tmp[0]
    annotation = tmp[-1]
    entrez[gene_id].append(annotation)
    
for line in open(mapping_file):
    up, eg = line.split()
    mapping_Uniprot_Entrez[up].append(eg)

max_ann = 0
prot = ''
for k in uniprot:
    annotations = set([])
    for eg in mapping_Uniprot_Entrez[k]:
        if eg in entrez:
            annotations = annotations.union(entrez[eg])
    if len(annotations) == 0:
        print "%s\tno-annotation"%k
    else:            
        print "%s\t%s"%(k,','.join(annotations))
        if len(annotations) > max_ann:
            max_ann = len(annotations)
            prot = k
        pass
print max_ann, prot

        
