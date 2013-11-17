#! /usr/bin/env python

import out

try:
  # import stuff
  #from Bio import SeqIO
  import argparse, blast, hhblits, map, hpoParser
  
  # do commandline parsing
  # "", "", action=[store, store_true], dest=varname, type=[int, str, ...], help=..., choices=[0, 1, 2], default=0, required=False/True
  # nargs="+" (arg must be giveb), "?"(arg optional)
  # metavar='N' extended argument
  # group = parser.add_mutually_exclusive_group()
  # group.add_argument("-v", "--verbose", action="store_true")
  # group.add_argument("-q", "--quiet", action="store_true")
  # 
  # 
  parser = argparse.ArgumentParser(description='This program should predict the function of proteins.')
  group = parser.add_mutally_exclusive_group()
  group.add_argument("-s", "--seq", action="store", dest="sequence", type=str, help="The seuqence in one letter code to predict the function for!")
  group.add_argument("-f", "--file", action="store", dest="fastaFile", type=str, help="A fasta file containing the protein sequences to predict there functions!")
  args = parser.parse_args()
  
  # init output
#  out.supressMessage = args.supMsg
#  out.supressDebug = args.supDbg
#  out.supressLog = args.supLog
#  out.supressWarning = args.supWarn
#  out.supressError = args.supErr
#  out.supressOutput = args.supOut
#  out.outputFormat = args.outForm
  
  # do stuff
  blastObj = blast.Blast.localBlast(seq=args.seq)
  for dict in blastObj.hits[:int(args.kNearest)]:
    print dict["hit_id"]
  
  # open the fasta file with the sequences for which to predict the sequence
  
except Exception as err:
  # main routine exception handler
  out.writeError(err)
