#! /usr/bin/env python

import out

try:
  # import stuff
  from Bio import SeqIO
  import argparse, blast, hhblits, map, hpoParser, os, blast, hhblits, sys, predictor
  
  # do commandline parsing
  parser = argparse.ArgumentParser(description='This program should predict the function of proteins.')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("-s", "--seq", action="store", dest="sequence", type=str, help="The seuqence in one letter code to predict the function for!")
  group.add_argument("-f", "--file", action="store", dest="fastaFile", type=str, help="A fasta file containing the protein sequences to predict there functions!")
  parser.add_argument("--svg", action="store_true", dest="createSvgImage", help="whether to create a svg image of the graph!")
  parser.add_argument("-v", "--verbose", dest="verbosity", type=int, default=0, required=False, help="set the verbosity of streams as sum 1=Message, 2=Debug, 4=Log, 8=Warning, 16=Error, 32=Output!")
  parser.add_argument("-w", "--outFormat", dest="outputFormat", type=str, choices=["bash", "plain", "html"], default="bash", required=False, help="set the output format to bash, plain or html!")
  parser.add_argument("-p", "--hpoFile", dest="hpoFile", type=str, default="../data/hp.obo", required=False, help="The path to the file with the current hpo definition!")
  parser.add_argument("-b", "--blastDb", dest="blastDbFile", type=str, default="../data/genes_UniProt.fasta", required=False, help="The path to the blast database to search with!")
  parser.add_argument("-l", "--hhblitsDb", dest="hhblitsDbFile", type=str, default="../data/PP2db", required=False, help="The path to the hhblits db file!")
  parser.add_argument("-c", "--uniprot2Hpo", dest="uni2hpo", type=str, default="../data/UniProt_2_HPO", required=False, help="A dictionary file for converting sequence identifiers to HPO-Terms!")
  parser.add_argument("-e", "--blastMinEVal", dest="blastMinEVal", type=float, default=1.0, required=False, help="The minimal E-Value all hits should have (default = 1)!")
  parser.add_argument("-n", "--neuronalNetwork", dest="neuronalNet", type=str, default="../data/neuronalNetwork.dat", required=False, help="The file containing the neuronal network that should be used by the predictor!")
  parser.add_argument("--minConf", dest="minimalConfidence", type=float, default=0.0, required=False, help="The minimal confidance value an accepted node should have; [from -2 to 2] (default: 0.0)!")
  args = parser.parse_args()
  
  # init output format
  out.supressMessage = bool(args.verbosity >> 0 & 1)
  out.supressDebug = bool(args.verbosity >> 1 & 1)
  out.supressLog = bool(args.verbosity >> 2 & 1)
  out.supressWarning = bool(args.verbosity >> 3 & 1)
  out.supressError = bool(args.verbosity >> 4 & 1)
  out.supressOutput = bool(args.verbosity >> 5 & 1)
  out.outputFormat = args.outputFormat

  # init the hpoParser
  out.writeLog("Build hpoGraph from file")
  hpoGraph = None
  if os.path.isfile(args.hpoFile):
    hpoGraph = hpoParser.HpoGraph(hpoFile=args.hpoFile)
  else:
    out.writeLog("missing hpoFile! Try standard hpoFile in the data directory")
    hpoGraph = hpoParser.HpoGraph()
  
  # init the hpo-identifier dict
  out.writeLog("Build uniprot 2 hpo dictionary")
  uni2hpoDict = {}
  f = open( args.uni2hpo, "r" )
  for line in f:
    line = line.strip()
    uni2hpoDict.update( { line.split("\t")[0] : line.split("\t")[1].split(",") } )
  f.close()
  
  # prediction method
  def predictSequence(args, hpoGraph, uni2hpoDict, name="Sequence", seq=""):
    # ok, do the whole thing
    try:
      # debug msg
      out.writeLog( "Predict function for protein: id: \"" + str( name ) +  "\" sequence: \"" + str( seq ) +"\"" )
      
      # ok, first of all, get similar sequences!
      blastResults = blast.Blast.localBlast(seq=seq, database=args.blastDbFile, minEVal=args.blastMinEVal)
      for hit in blastResults.hits:
        out.writeDebug( "Blast: found hit: " + str( hit ) )
      hhblitsResults = hhblits.HHBLITS.localHHBLITS(seq=str(seq), database=args.hhblitsDbFile)
      for hit in hhblitsResults.hits:
        out.writeDebug( "hhblits: found hit: " + str( hit ) )
      
      # now get the hpo-Identifiers for each similar sequence
      out.writeLog("uniprot ids ({}) 2 HPO Terms".format( len(blastResults.hits) + len(hhblitsResults.hits) ))
      for hit in blastResults.hits:
        try:
# Do not output this, it might be some GB output
#          out.writeDebug("found hpoTerms for " + str( hit[ "hit_id" ] ) + ": " + str( uni2hpoDict[ hit[ "hit_id" ] ] ) )
          hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )
        except KeyError:
          out.writeWarning( "MISSING HPO TERMS FOR HIT: " + str( hit ) )
      for hit in hhblitsResults.hits:
        try:
#          out.writeDebug("found hpoTerms for " + str( hit[ "hit_id" ] ) + ": " + str( uni2hpoDict[ hit[ "hit_id" ] ] ) )
          hit.update( { "hpoTerms" : uni2hpoDict[ hit[ "hit_id" ] ] } )
        except KeyError:
          out.writeWarning( "MISSING HPO TERMS FOR HIT: " + str( hit ) )
      
      # build and merge trees
      out.writeLog("Build and merge tree for similar sequences!")
      graph, hit_id = hpoGraph.getHpoSubGraph( hpoGraph.getRoot() ), 0
      for hit in blastResults.hits:
#        out.writeDebug("@blast merging: {}".format(hit))
        subtree = hpoGraph.getHpoSubGraph( hit[ 'hpoTerms' ], { hit_id : hit } )
        hit_id += 1
        graph += subtree
      for hit in hhblitsResults.hits:
#        out.writeDebug("@hhblits merging: {}".format(hit))
        subtree = hpoGraph.getHpoSubGraph( hit[ 'hpoTerms' ], { hit_id : hit } )
        hit_id += 1
        graph += subtree
      
      # do the prediciton
      out.writeLog("Run main prediction!")
      # init the predictor
      p = predictor.Predictor(args.neuronalNet)
      p.runprediction(seq, graph)
      # always accept the root
      for root in hpoGraph.getRoot():
        graph.getHpoTermById(root).accepted = 1
      
      # do the output
      out.writeLog("writing output")
      for node in graph.getAcceptedNodes( args.minimalConfidence ):
        out.writeOutput("{}\t{}\t{}".format(name, node.id, "%.*f" % (2, (node.accepted + 2) / 4)))
      
      # svg image desired?
      if args.createSvgImage:
        out.writeLog("Create a svg image showing all results!")
        if graph != None:
          graph.writeSvgImage(fileName = str( name ) + ".svg" )
        else:
          out.writeWarning( "Can't create a svg image from an empty tree!" )
      
      # clear attrs from all tree nodes, so that these don't interfere with later predictions
#      out.writeLog("Clear memory for next prediction")
#      hpoGraph.clearAttr()
      
    except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      out.writeError("Predicting Error: " + str( err ) + " on line: " + str( exc_tb.tb_lineno ) )
      exit(1)
    pass
  
  # printheader output
  out.writeOutput("AUTHOR TEAM_NAME")
  out.writeOutput("MODEL\t1")
  out.writeOutput("KEYWORDS clinical data, synteny.")
  
  # ok, do the whole thing
  if args.sequence != None:
    predictSequence(args, hpoGraph, uni2hpoDict, seq=args.sequence)
  elif os.path.isfile(args.fastaFile):
    f = open(args.fastaFile, "rU")
    for record in SeqIO.parse(f, "fasta"):
      predictSequence(args, hpoGraph, uni2hpoDict, name=record.id, seq=str(record.seq))
    f.close()
  else:
    out.writeError("Error: no sequence to predict given! (wrong path?)")
  
  out.writeOutput("END")
  
  # quit without error code
  exit(0)
  
except Exception as err:
  # main routine exception handler
  out.writeError("Unexpected Error: " + str( err ) )
  exit(1)
