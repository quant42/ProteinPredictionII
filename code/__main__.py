#! /usr/bin/env python

import out

try:
  # import stuff
  from Bio import SeqIO
  import argparse
  import blast
  
  # do commandline parsing
  parser = argparse.ArgumentParser(description='Program to predict the function of proteins.')
#  parser.add_option("-m", "--supressMessage", dest="supMsg")
#  parser.add_option("-d", "--supressDebug", dest="supDbg")
#  parser.add_option("-l", "--supressLog", dest="supMsg")
#  parser.add_option("-w", "--supressWarning", dest="supDbg")
#  parser.add_option("-e", "--supressError", dest="supMsg")
#  parser.add_option("-o", "--supressOutput", dest="supDbg")
#  parser.add_option("-f", "--outputFormat", dest="supDbg")
  
  # open the fasta file with the sequences for which to predict the sequence
  
  
  
except Exception as err:
  # main routine exception handler
  out.writeError(err)
