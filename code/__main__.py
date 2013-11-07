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
  parser.add_argument("-m", "--supressMessage", action="store_true", dest="supMsg")
  parser.add_argument("-d", "--supressDebug", action="store_true", dest="supDbg")
  parser.add_argument("-l", "--supressLog", action="store_true", dest="supLog")
  parser.add_argument("-w", "--supressWarning", action="store_true", dest="supWarn")
  parser.add_argument("-e", "--supressError", action="store_true", dest="supErr")
  parser.add_argument("-o", "--supressOutput", action="store_true", dest="supOut")
  parser.add_argument("-f", "--outputFormat", action="store", dest="outForm", default="bash")
  args = parser.parse_args()
  
  # init output
  out.supressMessage = args.supMsg
  out.supressDebug = args.supDbg
  out.supressLog = args.supLog
  out.supressWarning = args.supWarn
  out.supressError = args.supErr
  out.supressOutput = args.supOut
  out.outputFormat = args.outForm
  
  # do stuff
  blastObj = blast.Blast.localBlast(seq=args.seq)
  for dict in blastObj.hits[:int(args.kNearest)]:
    print dict["hit_id"]
  
  # open the fasta file with the sequences for which to predict the sequence
  
except Exception as err:
  # main routine exception handler
  out.writeError(err)
