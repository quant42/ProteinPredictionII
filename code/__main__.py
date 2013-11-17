#! /usr/bin/env python

import out

try:
  # import stuff
  from Bio import SeqIO
  import argparse, blast, hhblits, map, hpoParser, os
  
  # do commandline parsing
  parser = argparse.ArgumentParser(description='This program should predict the function of proteins.')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("-s", "--seq", action="store", dest="sequence", type=str, help="The seuqence in one letter code to predict the function for!")
  group.add_argument("-f", "--file", action="store", dest="fastaFile", type=str, help="A fasta file containing the protein sequences to predict there functions!")
  parser.add_argument("--svg", action="store_true", dest="createSvgImage", help="whether to create a svg image of the graph!")
  parser.add_argument("-d", "--debug", dest="debugFile", type=str, default=None, required=False, help="The debug file to write the debug/log/error messages to! (default: stderr)")
  parser.add_argument("-v", "--verbose", dest="verbosity", type=int, default=0, required=False, help="set the verbosity of streams as sum 1=Message, 2=Debug, 4=Log, 8=Warning, 16=Error, 32=Output!")
  parser.add_argument("-w", "--outFormat", dest="outputFormat", type=str, choices=["bash", "plain", "html"], default="bash", required=False, help="set the output format to bash, plain or html!")
  parser.add_argument("-p", "--hpoFile", dest="hpoFile", type=str, default="../data/hp.obo", required=False, help="The path to the file with the current hpo definition!")
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
  hpoGraph = None
  if os.path.isfile(args.hpoFile):
    hpoGraph = hpoParser.HpoGraph(hpoFile=args.hpoFile)
  else:
    out.writeLog("missing hpoFile! Try standard hpoFile in the data directory")
    hpoGraph = hpoParser.HpoGraph()
  
  # prediction method
  def predictSequence(args, hpoGraph, name="Sequence", seq=""):
    # ok, do the whole thing
    try:
      # debug msg
      out.writeDebug( "Predict function for protein: id: \"" + str( name ) +  "\" sequence: \"" + str( seq ) +"\"" )
      
      # ok, first of all, get similar sequences!
      
      # build the trees
      
      # do the prediciton
      
      # svg image desired?
      
      # clear attrs from all tree nodes, so that these don't interfere with later predictions
      hpoGraph.clearAttr()
      
    except Exception as err:
      out.writeError("Predicting Error: " + err)
      exit(1)
    pass
  
  # ok, do the whole thing
  if args.sequence != None:
    predictSequence(args, hpoGraph, seq=args.sequence)
  elif os.path.isfile(args.fastaFile):
    f = open(args.fastaFile, "rU")
    for record in SeqIO.parse(f, "fasta"):
      predictSequence(args, hpoGraph, name=record.id, seq=record.seq)
    f.close()
  else:
    out.writeError("Error: no sequence to predict given! (wrong path?)")
  
  # quit without error code
  exit(0)
  
except Exception as err:
  # main routine exception handler
  out.writeError("Unexpected Error: " + err)
  exit(1)
