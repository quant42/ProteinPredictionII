#! /usr/bin/env python

# imports
import out, commands, re

# the blast class
class Blast():
  
  """ A basic blasting class """
  
  # construct this class by the xml blast output
  def __init__(self, blastResults):
    out.writeDebug("Initalize Blast Alignment by blasting results ...")
    # self stuff
    self.hits = []
    # parse the blast results
    hitPattern = re.compile("<Hit>(.*?)</Hit>", re.DOTALL)
    hitIdPattern = re.compile("<Hit_def>(.*?)</Hit_def>")
    hitEValPattern = re.compile("<Hsp_evalue>(.*?)</Hsp_evalue>")
    hitFromPattern = re.compile("<Hsp_hit-from>(.*?)</Hsp_hit-from>")
    hitToPattern = re.compile("<Hsp_hit-to>(.*?)</Hsp_hit-to>")
    # for each hit in the xml
    for hit in hitPattern.finditer( blastResults ):
      text = hit.group(0)
      hit_id = hitIdPattern.search( text ).group( 1 )
      hit_e_value = hitEValPattern.search( text ).group( 1 )
      hit_from = hitFromPattern.search( text ).group( 1 )
      hit_to = hitToPattern.search( text ).group( 1 )
      self.hits.append({'hit_id':hit_id, 'hit_value': float(hit_e_value), 'hit_from':int(hit_from), 'hit_to': int(hit_to), 'hit_order': False, 'method':'blast'})
  
  @staticmethod
  def localBlast(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP", database = "../data/genes_UniProt.fasta", minEVal = 1):
    out.writeDebug( "Do a local blast search for {} in {}".format( seq, database ) )
    blastResults = commands.getstatusoutput( "echo \"{}\" | blast2 -p blastp -d {} -N -e {} -m 7".format( seq, database, minEVal ) )
    if blastResults[0] != 0:
      out.writeLog("Return code for blast search {} in {} returned with exit code {}!".format( seq, database, blastResults[0] ) )
    return Blast( blastResults[1] )

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  content = ""
  f = file("test.xml", "r")
  for line in f:
    content += line
  f.close()
  b = Blast( content )
  print b.hits 
#  Blast.localBlast()

