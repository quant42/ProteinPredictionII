#!/usr/bin/env python

import blast, hhblits, pybrain, features, out, hpoParser, gzip
from Bio import SeqIO
from predictor import Predictor

out.supressMessage = True
out.supressDebug = True
out.supressLog = True
out.supressWarning = True
out.supressError = False
out.supressOutput = False
out.outputFormat = 'bash'

blastDbFile = '../data/genes_UniProt.fasta'
hhblitsDbFile = '../data/PP2db.cs219'
hpoFile = '../data/hp.obo'
hpoMappingFile = '../data/UniProt_2_HPO_full'
targetFile = '../data/sp_species.9606.all_.noexp_.tfa_.gz'
neuralNetworkFile = '../data/NeuralNetwork'

neuralNet = Predictor(None)
hpoGraph = hpoParser.HpoGraph(hpoFile)

def predictTargets():
    uni2hpoDict = {}
    f = open(hpoMappingFile)
    for line in f:
        line = line.strip()
        uni2hpoDict.update( { line.split("\t")[0] : line.split("\t")[1].split(",") } )
    f.close()
    
    for record in SeqIO.parse(gzip.open(targetFile, 'rb'), "fasta") :
        terms = predictSequence(hpoGraph, uni2hpoDict, name=record.id, seq=record.seq, predictor = neuralNet)

        for term, confidence, in terms:
            print "%s\t%s\t%s"%(record.id, term, confidence)


def predictSequence(hpoGraph, uni2hpoDict, name="Sequence", seq="", predictor = ''):
    import blast, hhblits
    # similar sequence
    blastResults = blast.Blast.localBlast(seq=seq, database=blastDbFile)
    hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=seq, database=hhblitsDbFile)
    
    # now get the hpo-Identifiers for each similar sequence
    for hit in blastResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )
    for hit in hhblitsResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )    
    # build and merge trees
    graph, hit_id = None, 0
    
    for hit in blastResults.hits:
        subtree = hpoGraph.getHpoSubGraph( hit[ 'hpoTerms' ], { hit_id : hit } )
        hit_id += 1
        if graph == None:
            graph = subtree
        else:
            graph += subtree
            
    for hit in hhblitsResults.hits:
        subtree = hpoGraph.getHpoSubGraph( hit[ 'hpoTerms' ], { hit_id : hit } )
        hit_id += 1
        if graph == None:
            graph = subtree
        else:
            graph += subtree
  
    # do the prediction
    terms = set([])
    if graph != None:
        predictor.runprediction(seq, graph)
        for nodeID, node in graph.hpoTermsDict.iteritems():
            if nodeID == 'HP:0000001':
                continue
            # get the nodes
            terms.add((node.id, node.accepted))
    hpoGraph.clearAttr()

    # return the set containing the most specific predictions
    return terms

predictTargets()
