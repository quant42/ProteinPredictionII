from collections import defaultdict

"""implements the function get_annotation_mapping which returns 
a dictionary of mappings from Uniprot AC to HPO terms 
get_annotation_mapping can be called with an option 'reduced' to return 
either all terms (False) or only the most specific terms (True)"""

def get_hpo_tree(filename):
    tree = {}
    node_id = ''
    for line in open(filename):
        if line.startswith('id:'):
            node_id = line.split()[-1]
            tree[node_id] = {'childnodes': [],'parentnodes': [], 'visited': 0}
        #TODO skip obsolete nodes
        elif line.startswith('is_obsolete:'):
            del tree[node_id]
            
    for line in open(filename):
        if line.startswith('id:'):
            node_id = line.split()[-1]
        elif line.startswith('is_a:') and node_id in tree:
            parentnode = line.split()[1]
            tree[node_id]['parentnodes'].append(parentnode)
            tree[parentnode]['childnodes'].append(node_id)
    return tree

def has_children(tree, node_id, set_of_children):
    for child in tree[node_id]['childnodes']:
        if child in set_of_children:
            return True
        elif has_children(tree, child, set_of_children):
            return True
    return False

def get_annotation_mapping(reduced = True):
    fasta_file = '../data/genes_UniProt.fasta'
    annotation_file = '../data/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
    mapping_file = '../data/automatic_mapping'
    hpo_file = '../data/hp.obo'
    mapping_Uniprot_Entrez = defaultdict(list)
    REDUCE = reduced

    uniprot = {}
    hpo_tree = get_hpo_tree(hpo_file)
        
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
    mapping_dict = {}
    for k in uniprot:
        annotations = set([])
        for eg in mapping_Uniprot_Entrez[k]:
            if eg in entrez:
                annotations = annotations.union(entrez[eg])
        reduced_annotations = set([])
        for node in annotations:
            if not has_children(hpo_tree, node, annotations):
                reduced_annotations.add(node)
        if len(annotations) == 0:
            print "%s\tno-annotation"%k
        else:
            if REDUCE:
                #print "%s\t%s"%(k,','.join(reduced_annotations))
                mapping_dict[k] = reduced_annotations
            else:
                #print "%s\t%s"%(k,','.join(annotations))
                mapping_dict[k] = annotations
    return mapping_dict

if __name__ == "__main__":
     if 63 == len(get_annotation_mapping(False)['O95255']) and 53 == len(get_annotation_mapping(True)['O95255']):
         print 'tests successfull'
            
