#!/usr/bin/env python

from Bio import SeqIO
from random import shuffle
import out

# init output format
out.supressMessage = True
out.supressDebug = False
out.supressLog = True
out.supressWarning = True
out.supressError = False
out.supressOutput = False
out.outputFormat = 'bash'

blastDbFile = '../data/genes_UniProt.fasta'
hhblitsDbFile = '../data/PP2db.cs219'
hpoFile = '../data/hp.obo'
hpoMappingFile = '../data/UniProt_2_HPO_full'
reducedFile = '../data/genes_UniProt_reduced_80.fasta'
clusterFile = '../data/genes_UniProt_reduced_80.cluster'


# use set of sequences with reduced sequenc redundancy as basis for validation
# set created with CD-HIT at 80% sequence similarity
out.writeDebug('Prepare sequence similarity reduced data set from %s'%reducedFile)
reduced_sequences = []

for record in SeqIO.parse(open(reducedFile), 'fasta'):
    reduced_sequences.append((record.id, record.seq))
shuffle(reduced_sequences)

# also take care to reserve sequences that are in the same cluster as the test sequences

out.writeDebug('Digest sequence clusterings from %s'%clusterFile)
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
sequenceCluster[representative] = sequences    


def cross_validate(sequences, folds = 10):
    import hpoParser

    dataset_size = len(sequences)
    errorMeasures = []

    # init the hpoParser
    hpoGraph = hpoParser.HpoGraph(hpoFile)

    # init the hpo-identifier dict
    out.writeDebug('Initialize dictionary with true annotations from %s'%hpoMappingFile)
    uni2hpoDict = {}
    f = open(hpoMappingFile)
    for line in f:
        line = line.strip()
        uni2hpoDict.update( { line.split("\t")[0] : line.split("\t")[1].split(",") } )
    f.close()

    # create folds
    for i in range(folds):
        out.writeDebug('Start with fold %s from %s'%(i+1, folds))
        # test fold
        test = sequences[i:dataset_size:folds]
        # fold to learn parameters
        crossTrain = sequences[(i+1)%folds:dataset_size:folds]
        # fold to train on, does not include the redundant sequences here
        # is not really necessary, since train and crosstrain are preserved
        train = []
        for j in range(folds):
            if j != i and j != (i+1)%folds:
                train = train + sequences[j:dataset_size:folds]
        dataset = {'train': train, 'crossTrain': crossTrain, 'test': test}
        # learn the parameters, however they will look
        # parameters should be neural net to recognize valid annotation
        predictor = learn_parameters(hpoGraph, uni2hpoDict, dataset)
        # test the parameters on the independent test fold
        errorMeasures.append(predict_set(hpoGraph, uni2hpoDict, dataset, predictor))
    for fold, f in enumerate(errorMeasures):
        try:
            precision = f[0]/float(f[0]+f[1])
            recall = f[0]/float(f[0]+f[2])
            print 'fold %s:\nprecision: %s\nrecall: %s'%(fold, precision, recall)
        except ZeroDivisionError, e:
            out.writeDebug('Division by Zero.\nTP, FP, FN are: &s, &s, &s'%(f[0], f[1], f[2]))
            
def learn_parameters(hpoGraph, uni2hpoDict, dataset):
    out.writeDebug('Start training the predictor.')
    from predictor import Predictor
    neuralNet = Predictor(None)
    # in crosstraining, the test set is the crossTrain and the crossTrain set is the (here ignored) test set
    crossTrainSet = {'train': dataset['train'], 'crossTrain': dataset['test'], 'test': dataset['crossTrain']}
    trainingNodes = train_result_set(hpoGraph, uni2hpoDict, crossTrainSet)

    out.writeDebug('Collected all the nodes for training')
    neuralNet.trainprediction(trainingNodes)

    return neuralNet

def train_result_set(hpoGraph, uni2hpoDict, dataset):
    trainingNodes = []
    for sequence_id, sequence in dataset['test']:
        trainingNodes += train_result_Sequence(hpoGraph, uni2hpoDict, dataset, name=sequence_id, seq=sequence)
    return trainingNodes

def train_result_Sequence(hpoGraph, uni2hpoDict, dataset, name='', seq=''):
    out.writeDebug('Get training data for sequence name %s with sequence: %s'%(name, seq))

    import blast, hhblits
    # similar sequence
    blastResults = blast.Blast.localBlast(seq=seq, database=blastDbFile)
    hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=str(seq), database=hhblitsDbFile)
    
    # now get the hpo-Identifiers for each similar sequence
    for hit in blastResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )
    for hit in hhblitsResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )

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
            out.writeDebug('Skip hit %s in database that is in the test data'%(hit['hit_id']))
            continue
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

    
    
    # get training nodes
    trainingNodes = []
    if graph != None:
        for node in graph.hpoTermsDict:
            
            ValidPrediction = False
            if node in uni2hpoDict[name]:
                ValidPrediction = True
            # copy node attributes for training
            trainingNodes.append((graph.hpoTermsDict[node].copy(), ValidPrediction))
            
    hpoGraph.clearAttr()

    # return the set of trainings nodes with target variable
    return trainingNodes    

def predict_set(hpoGraph, uni2hpoDict, dataset, predictor):
    TP, FP, FN = 0, 0, 0
    
    # predict test set
    for sequence_id, sequence in dataset['test']:
        predictedHpoTerms = predictSequence(hpoGraph, uni2hpoDict, dataset, name=sequence_id, seq=sequence, predictor=predictor)
        (thisTP, thisFP, thisFN) = validateTerms(predictedHpoTerms, sequence_id, uni2hpoDict)
        TP += thisTP
        FP += thisFP
        FN += thisFN
    return (TP, FP, FN)
                              
def predictSequence(hpoGraph, uni2hpoDict, dataset, name="Sequence", seq="", predictor = ''):
    import blast, hhblits
    # similar sequence
    blastResults = blast.Blast.localBlast(seq=seq, database=blastDbFile)
    hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=seq, database=hhblitsDbFile)
    
    # now get the hpo-Identifiers for each similar sequence
    for hit in blastResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )
    for hit in hhblitsResults.hits:
        hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )

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
            # get the accepted nodes
            if node.accepted:
                terms.add(node)
    hpoGraph.clearAttr()

    # return the set containing the most specific predictions
    return terms

def validateTerms(predictedHpoTerms, sequence_id, uni2hpoDict):
    TP = 0
    FP = 0
    FN = 0
    for term in predictedHpoTerms:
        if term.id in uni2hpoDict[sequence_id]:
            TP += 1
        else:
            FP += 1
    FN = len(uni2hpoDict[sequence_id]) - TP     
    
    return (TP, FP, FN)
    
    
cross_validate(reduced_sequences, 10)
