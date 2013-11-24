#!/usr/bin/env python

from Bio import SeqIO
from random import shuffle

blastDbFile = '../data/genes_UniProt.fasta'
hhblitsDbFile = '../data/PP2db.cs219'
hpoFile = '../data/hp.obo'
hpoMappingFile = '../data/UniProt_2_HPO'
reducedFile = '../data/genes_UniProt_reduced_80.fasta'
clusterFile = '../data/genes_UniProt_reduced_80.cluster'


# use set of sequences with reduced sequenc redundancy as basis for validation
# set created with CD-HIT at 80% sequence similarity
reduced_sequences = []

for record in SeqIO.parse(open(reducedFile), 'fasta'):
    reduced_sequences.append((record.id, record.seq))
shuffle(reduced_sequences)

# also take care to reserve sequences that are in the same cluster as the test sequences

sequenceCluster = {}
representative = ''
sequences = set([])
for line in open(clusterFile):
    if not line.strip():
        continue
    if  line.startswith('>'):
        #new cluster:
        if representative:
            sequenceCluster[representative] = sequences

        representative = ''
        sequences = set([])
    else:
        sequence = line.split('>')[1].split('.')[0]
        sequences.add(sequence)
        if '*' in line:
            #representative sequences have a star
            representative = sequence
    


def cross_validate(sequences, folds = 10):    
    import out, hpoParser

    dataset_size = len(sequences)
    errorMeasures = []

    # init output format
    out.supressMessage = True
    out.supressDebug = True
    out.supressLog = True
    out.supressWarning = True
    out.supressError = False
    out.supressOutput = False
    out.outputFormat = 'bash'

    # init the hpoParser
    hpoGraph = hpoParser.HpoGraph(hpoFile)

    # init the hpo-identifier dict
    uni2hpoDict = {}
    f = open(hpoMappingFile)
    for line in f:
        line = line.strip()
        uni2hpoDict.update( { line.split("\t")[0] : line.split("\t")[1].split(",") } )
    f.close()

    # create folds
    for i in range(folds):
        # test fold
        test = sequences[i:dataset_size:folds]
        # fold to learn parameters
        crossTrain = sequences[(i+1)%folds:dataset_size:folds]
        # fold to train on, does not include the redundant sequences here
        train = []
        for j in range(folds):
            if j != i and j != (i+1)%folds:
                train = train + sequences[j:dataset_size:folds]
        dataset = {'train': train, 'crossTrain': crossTrain, 'test': test}
        # learn the parameters, however they will look
        parameters = learn_parameters(hpoGraph, uni2hpoDict, dataset)
        
        # test the parameters on the independent test fold
        errorMeasures.append((len(test), predict_set(hpoGraph, uni2hpoDict, dataset, parameters)))

def learn_parameters(hpoGraph, uni2hpoDict, dataset):
    minCombinedScore, minNumberOfHits, level = 0, 0, 0
    # in crosstraining, the test set is the crossTrain and the crossTrain set is the (here ignored) test set
    crossTrainSet = {'train': dataset['train'], 'crossTrain': dataset['test'], 'test': dataset['crossTrain']}
    bestResult = 0
    for comScore in range(11):
        for numHits in range(10):
            for depth in range(10):
                error = predict_set(hpoGraph, uni2hpoDict, crossTrainSet, (comScore/float(10), numHits, depth))

    return (minCombinedScore, minNumberOfHits)

def predict_set(hpoGraph, uni2hpoDict, dataset, parameters):
    errorMeasures = []
    
    # predict test set
    for sequence_id, sequence in dataset['test']:
        predictedHpoTerms = predictSequence(hpoGraph, uni2hpoDict, dataset, name=sequence_id, seq=sequence, parameters=parameters)
        break
        quality = validateTerms(predictedHpoTerms, sequence_id, uni2hpoDict)

    return errorMeasures
                              
def predictSequence(hpoGraph, uni2hpoDict, dataset, name="Sequence", seq="", parameters = (0.5,3, 20)):
    import blast, hhblits
    # similar sequence
    blastResults = blast.Blast.localBlast(seq=seq, database=blastDbFile)
    #hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=seq, database=hhblitsDbFile)
    
    # now get the hpo-Identifiers for each similar sequence
    for hit in blastResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )
    #for hit in hhblitsResults.hits:
    #    hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )

    # set of hits to ignore to avoid information leakage
    reserved = set([])

    # add the sequences in the associated clusters
    for representative, sequence in dataset['crossTrain']:
        reserved = reserved | sequenceCluster[representative]
        
    for representative, sequence in dataset['test']:
        reserved = reserved | sequenceCluster[representative]   

    
    # build and merge trees
    graph, hit_id = None, 0
    
    for hit in blastResults.hits:
        #take only hits from the training set, ignore hits from test or crosstrain set
        if hit['hit_id'] in reserved:
            continue
        subtree = hpoGraph.getHpoSubGraph( hit[ 'hpoTerms' ], { hit_id : hit } )
        hit_id += 1
        if graph == None:
            graph = subtree
        else:
            graph += subtree
    #for hit in hhblitsResults.hits:
    #    subtree = hpoGraph.getHpoSubGraph( hit[ 'hpoTerms' ], { hit_id : hit } )
    #    hit_id += 1
    #    if graph == None:
    #        graph = subtree
    #    else:
    #        graph += subtree
  
    # do the prediction
    terms = set([])
    if graph != None:
        for node in graph.hpoTermsDict:
            combinedValue = 1
            for hit_number, hit_attributes in graph.hpoTermsDict[ node ].attributes.iteritems():
                combinedValue *= hit_attributes['hit_value']

            if combinedValue <= parameters[0] or len(graph.hpoTermsDict[ node ].attributes) > parameters[1]:
                graph.hpoTermsDict[ node ].accepted = True
                # remove parent nodes of the accepted node
                for parentNode in graph.getParents(node):
                    if parentNode in terms:
                        terms.remove(parentNode)
                # add node only, if no child nodes are in the set
                moreSpecific = False
                for childNode in graph.getAllChildren(node):
                    if childNode in terms:
                        moreSpecific = True
                        break
                if not moreSpecific:
                    # TODO: add confidence score
                    terms.add(node)
    hpoGraph.clearAttr()

    # return the set containing the most specific predictions
    return terms

def validateTerms(predictedHpoTerms, sequence_id, uni2hpoDict):
    # TODO: evaluation conditions? What is a correct prediction? Does every node in the correct subtree contribute equally?
    truePositive = 0
    falsePositive = 0
    moreGeneralTruePositive = 0
    moreSpecificTruePositive = 0
    return None
    
    
cross_validate(reduced_sequences, 10)
