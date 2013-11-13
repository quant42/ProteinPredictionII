#! /usr/bin/env python

# ===================================================================
# This class provides functions for searching for simmilar proteins
# with the blast algorithm. Therefor blast must be installed locally
# (Ubuntu: sudo apt-get install blast2) or the ncbi blast must be
# available.
# Call Blast.ncbiBlast(seq="") or Blast.localBlast(seq="", 
# database="") to do the blast alignments. You will get a Blast class
# which has an attribute alignments.
# ===================================================================
# sequence produces malformed xml_
# MGRGAGREYSPAATTAENGGGKKKQKEKELDELKKEVAMDDHKLSLDELGRKYQVDLSKGLTNQRAQDVLARDGPNALTPPPTTPEWVKFCRQLFGGFSILLWIGAILCFLAYGIQAAMEDEPSNDNLYLGVVLAAVVIVTGCFSYYQEAKSSKIMDSFKNMVPQQALVIREGEKMQINAEEVVVGDLVEVKGGDRVPADLRIISSHGCKVDNSSLTGESEPQTRSPEFTHENPLETRNICFFSTNCVEGTARGIVIATGDRTVMGRIATLASGLEVGRTPIAMEIEHFIQLITGVAVFLGVSFFVLSLILGYSWLEAVIFLIGIIVANVPEGLLATVTVCLTLTAKRMARKNCLVKNLEAVETLGSTSTICSDKTGTLTQNRMTVAHMWFDNQIHEADTTEDQSGATFDKRSPTWTALSRIAGLCNRAVFKAGQENISVSKRDTAGDASESALLKCIELSCGSVRKMRDRNPKVAEIPFNSTNKYQLSIHEREDSPQSHVLVMKGAPERILDRCSTILVQGKEIPLDKEMQDAFQNAYMELGGLGERVLGFCQLNLPSGKFPRGFKFDTDELNFPTEKLCFVGLMSMIDPPRAAVPDAVGKCRSAGIKVIMVTGDHPITAKAIAKGVGIISEGNETVEDIAARLNIPMSQVNPREAKACVVHGSDLKDMTSEQLDEILKNHTEIVFARTSPQQKLIIVEGCQRQGAIVAVTGDGVNDSPALKKADIGIAMGISGSDVSKQAADMILLDDNFASIVTGVEEGRLIFDNLKKSIAYTLTSNIPEITPFLLFIIANIPLPLGTVTILCIDLGTDMVPAISLAYEAAESDIMKRQPRNSQTDKLVNERLISMAYGQIGMIQALGGFFTYFVILAENGFLPSRLLGIRLDWDDRTMNDLEDSYGQEWTYEQRKVVEFTCHTAFFASIVVVQWADLIICKTRRNSVFQQGMKNKILIFGLLEETALAAFLSYCPGMGVALRMYPLKVTWWFCAFPYSLLIFIYDEVRKLILRRYPGGWVEKETYY


import out, commands, re
from xml.dom import minidom

class Blast():
  
  """ A basic blasting class """
  
  # constructor for building this class, if the header of the sequences, the sequences them self and the
  # corresponding blastResults are already known
  def __init__(self, blastResults):
    out.writeDebug("Initalize Blast Alignment by blasting results ...")
    # self stuff
    self.hits = []
    # parse the blast results
    begin = False
    for line in blastResults.split('\n'):
      if line.startswith('#'):
        begin = True
      elif begin:
        query_id, hit_id, perc_identity, alignment_length, mismatches, gap_openings, q_start, q_end, hit_from, hit_to, hit_e_value, bit_score = line.split('\t')

        self.hits.append({'hit_id':hit_id, 'hit_value': float(hit_e_value), 'hit_from':int(hit_from), 'hit_to': int(hit_to), 'hit_order': False})
    
  @staticmethod
  def localBlast(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP", database = "../data/genes_UniProt.fasta"):
    out.writeDebug( "Do a local blast search for {} in {}".format( seq, database ) )
    blastResults = commands.getstatusoutput( "echo \"%s\" | blast2 -p blastp -d ../data/genes_UniProt.fasta -N -m 9" % seq )
    if blastResults[0] != 0:
      out.writeLog("Return code for blast search {} in {} returned with exit code {}!".format( seq, database, blastResults[0] ) )
    return Blast( blastResults[1] )

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  Blast.localBlast()
