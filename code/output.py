#! /usr/bin/env python

import sys

# function controlling variables
supressDebug = False
supressLog = False
supressWarning = False
supressError = False
supressOutput = False

outputFormat = "bash" # possible values: bash, plain, html (default: bash)

# functions

def writeStdErr(string):
  if outputFormat == "plain":
    sys.stderr.write(string)
  elif outputFormat == "html":
    sys.stderr.write("<span class=\"errStream \"")
  else:

def writeDebug(string):
  if not supressDebug:
    if outputFormat == "plain":
      sys.stderr.write(string)
    elif outputFormat == "html":
      sys.stderr.write("<span class=\"stream errStream debugMessage\">%s</span>" % string)
    else:
      sys.stderr.write("\033[38;5;20m%s\033[0m\n" % string)

