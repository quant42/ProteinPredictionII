#! /usr/bin/env python

import out

try:
  # import stuff
  #from Bio import SeqIO
  import argparse
  import blast
  
  # do commandline parsing
  parser = argparse.ArgumentParser(description='Program to predict the function of proteins.')
  parser.add_argument("-k", "--k-nearest", action="store", dest="kNearest", default=5)
  parser.add_argument("-s", "--seq", action="store", dest="seq")
  parser.add_argument("-a", "--supressMessage", action="store_true", dest="supMsg")
  parser.add_argument("-b", "--supressDebug", action="store_true", dest="supDbg")
  parser.add_argument("-c", "--supressLog", action="store_true", dest="supLog")
  parser.add_argument("-d", "--supressWarning", action="store_true", dest="supWarn")
  parser.add_argument("-e", "--supressError", action="store_true", dest="supErr")
  parser.add_argument("-f", "--supressOutput", action="store_true", dest="supOut")
  args = parser.parse_args()
  
  # init output
  out.supressMessage = bool(args.supMsg)
  out.supressDebug = bool(args.supDbg)
  out.supressLog = bool(args.supLog)
  out.supressWarning = bool(args.supWarn)
  out.supressError = bool(args.supErr)
  out.supressOutput = bool(args.supOut)
  
  # do stuff
  blastObj = blast.Blast.localBlast(seq=args.seq)
  for dict in blastObj.hits[:int(args.kNearest)]:
    print dict["hit_id"]
  
  # open the fasta file with the sequences for which to predict the sequence
  
  
  
except Exception as err:
  # main routine exception handler
  out.writeError(err)
