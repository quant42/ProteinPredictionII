#! /usr/bin/env python

import sys

# function controlling variables
supressMessage = False
supressDebug = False
supressLog = False
supressWarning = False
supressError = False
supressOutput = False   # I know doesn't really made sense

outputFormat = "bash"   # possible values: bash, plain, html (default: bash)

# basic output functions
def writeMessage(string):
  if not supressMessage:
    if outputFormat != "html":
      sys.stderr.write("{}\n".format( string ) )
    else:
      sys.stderr.write("<span class=\"stream errStream messageMessage\">{}</span><br>".format ( string ) )

def writeDebug(string):
  if not supressDebug:
    if outputFormat == "plain":
      sys.stderr.write("{}\n".format( string ) )
    elif outputFormat == "html":
      sys.stderr.write("<span class=\"stream errStream debugMessage\">{}</span><br>\n".format( string ) )
    else:
      sys.stderr.write("\033[38;5;7m[DEBUG] {}\033[0m\n".format( string ) )

def writeLog(string):
  if not supressLog:
    if outputFormat == "plain":
      sys.stderr.write("{}\n".format( string ) )
    elif outputFormat == "html":
      sys.stderr.write("<span class=\"stream errStream logMessage\">{}</span><br>\n".format( string ) )
    else:
      sys.stderr.write("\033[38;5;10m[LOG] {}\033[0m\n".format( string ) )

def writeWarning(string):
  if not supressWarning:
    if outputFormat == "plain":
      sys.stderr.write("{}\n".format( string ) )
    elif outputFormat == "html":
      sys.stderr.write("<span class=\"stream errStream warningMessage\">{}</span><br>\n".format( string ) )
    else:
      sys.stderr.write("\033[38;5;11m[WARNING] {}\033[0m\n".format( string ) )

def writeError(string):
  if not supressError:
    if outputFormat == "plain":
      sys.stderr.write("{}\n".format( string ) )
    elif outputFormat == "html":
      sys.stderr.write("<span class=\"stream errStream errorMessage\">{}</span><br>\n".format( string ) )
    else:
      sys.stderr.write("\033[38;5;9m[ERROR] {}\033[0m\n".format( string ) )

def writeOutput(string):
  if not supressOutput:
    if outputFormat != "html":
      sys.stdout.write("{}\n".format( string ) )
    else:
      sys.stdout.write("<span class=\"stream outStream outputMessage\">{}</span><br>\n".format( string ) )

