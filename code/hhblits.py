#! /usr/bin/env python

# ===================================================================
# This class provides functions for searching for similar proteins
# with the hhblits tool. Therefore hhblits must be installed locally.
# Call HHBLITS.localHHBLITS(seq="", # database="") to do the hhblits
# search. You will get a class which has an attribute significant_hits.
# ===================================================================

import out, subprocess, re, os, math
minEValue = 0.01
class HHBLITS():
  
  """ A basic hmmblits class """
  
  # constructor for building this class, if the header of the sequences, the sequences them self and the
  # corresponding hhblitsResults are already known
  def __init__(self, hhblitsResults):
    out.writeDebug("Initalize hhblits alignment ...")      
    # self stuff
    self.hits = []
    if hhblitsResults == '#unknown error':
      return None
    # parse the hhblits results
    beginOfResults = False
    lines = hhblitsResults.split('\n')
    tmp = []
    for line in lines:
      # skip empty lines
      if not line.strip():
        continue
      # skip empty lines
      if line.find('Done') != -1:
        break
      # skip all lines before the actual searching results begin
      if beginOfResults:
        items = line.split()
        hit_id, hit_e_value, query_hit = items[1], items[3], items[9]
        hit_from, hit_to = query_hit.split('-')[:2]
        hit_to = hit_to.split('(')[0]
        self.hits.append({'hit_id':hit_id, 'hit_value': float(hit_e_value), 'hit_from':int(hit_from), 'hit_to': int(hit_to), 'hit_order': False})
      else:
        if line.find("No Hit") != -1:
          beginOfResults = True
    
    
  
  @staticmethod
  def localHHBLITS(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP", database = "/mnt/project/rost_db/data/hhblits/uniprot20_02Sep11"):
    import time
    out.writeDebug("Do a local hhblits search for {} in {}".format( seq, database ) )
    time_stamp = str(int(time.time()))
    seq_file = ''
    if re.match('^[A-Z]*$',seq):
      
      seq_file = 'hhblits_input_'+time_stamp
      fh = open(seq_file,'w')
      fh.write(seq)
      fh.close()
    else:
      seq_file = seq
    outfile = 'hhblits_'+time_stamp+'.out'
    command = "hhblits -i {} -o {} -d {} -e {}".format(seq_file, outfile, database, minEValue)
    try:
      hhblitsResults = subprocess.check_output(command, shell = True)
      hhblitsResults = open(outfile).read()
      os.remove(outfile)
    except subprocess.CalledProcessError as err:
      out.writeLog("Return code for blast search {} in {} returned with exit code {}!".format( seq, database, err.returncode ) )
      #hhblitsResults = open('../../stdoutput').read()
      hhblitsResults = ''
    if seq != seq_file:
      os.remove(seq_file)
    return HHBLITS(hhblitsResults)

def parseEValue(e_value):
# translate evalue text into float
  if 'E' in e_value:
    base, exponent = e_value.split('E')
    return float(base)*math.pow(10,int(exponent))
  else:
    return float(e_value)

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  HHBLITS.localHHBLITS()
