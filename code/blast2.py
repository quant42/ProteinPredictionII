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
#MGRGAGREYSPAATTAENGGGKKKQKEKELDELKKEVAMDDHKLSLDELGRKYQVDLSKGLTNQRAQDVLARDGPNALTPPPTTPEWVKFCRQLFGGFSILLWIGAILCFLAYGIQAAMEDEPSNDNLYLGVVLAAVVIVTGCFSYYQEAKSSKIMDSFKNMVPQQALVIREGEKMQINAEEVVVGDLVEVKGGDRVPADLRIISSHGCKVDNSSLTGESEPQTRSPEFTHENPLETRNICFFSTNCVEGTARGIVIATGDRTVMGRIATLASGLEVGRTPIAMEIEHFIQLITGVAVFLGVSFFVLSLILGYSWLEAVIFLIGIIVANVPEGLLATVTVCLTLTAKRMARKNCLVKNLEAVETLGSTSTICSDKTGTLTQNRMTVAHMWFDNQIHEADTTEDQSGATFDKRSPTWTALSRIAGLCNRAVFKAGQENISVSKRDTAGDASESALLKCIELSCGSVRKMRDRNPKVAEIPFNSTNKYQLSIHEREDSPQSHVLVMKGAPERILDRCSTILVQGKEIPLDKEMQDAFQNAYMELGGLGERVLGFCQLNLPSGKFPRGFKFDTDELNFPTEKLCFVGLMSMIDPPRAAVPDAVGKCRSAGIKVIMVTGDHPITAKAIAKGVGIISEGNETVEDIAARLNIPMSQVNPREAKACVVHGSDLKDMTSEQLDEILKNHTEIVFARTSPQQKLIIVEGCQRQGAIVAVTGDGVNDSPALKKADIGIAMGISGSDVSKQAADMILLDDNFASIVTGVEEGRLIFDNLKKSIAYTLTSNIPEITPFLLFIIANIPLPLGTVTILCIDLGTDMVPAISLAYEAAESDIMKRQPRNSQTDKLVNERLISMAYGQIGMIQALGGFFTYFVILAENGFLPSRLLGIRLDWDDRTMNDLEDSYGQEWTYEQRKVVEFTCHTAFFASIVVVQWADLIICKTRRNSVFQQGMKNKILIFGLLEETALAAFLSYCPGMGVALRMYPLKVTWWFCAFPYSLLIFIYDEVRKLILRRYPGGWVEKETYY


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
    self.xml_raw = minidom.parseString(blastResults)
    hitlist = self.xml_raw.getElementsByTagName('Hit') 
    for hit in hitlist:
      hit_id, hit_e_value, hit_from, hit_to = '', 0, -1, -1
      for child in hit.childNodes:
        if child.nodeName == 'Hit_def':
          hit_id = child.childNodes[0].nodeValue.split()[0]
        elif child.nodeName == 'Hit_hsps':
          for child2 in child.childNodes:
            if child2.nodeName == 'Hsp':
              for child3 in child2.childNodes:
                if child3.nodeName == 'Hsp_evalue':
                  hit_e_value = child3.childNodes[0].nodeValue
                elif child3.nodeName == 'Hsp_query-from':
                  hit_from = child3.childNodes[0].nodeValue
                elif child3.nodeName == 'Hsp_query-to':
                  hit_to = child3.childNodes[0].nodeValue
          break
          
      self.hits.append({'hit_id':hit_id, 'hit_e_value': float(hit_e_value), 'hit_from':int(hit_from), 'hit_to': int(hit_to)})
    
  @staticmethod
  def localBlast(seq = "NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP", database = "../data/genes_UniProt.fasta"):
    out.writeDebug( "Do a local blast search for {} in {}".format( seq, database ) )
    blastResults = commands.getstatusoutput( "echo \"%s\" | blast2 -p blastp -d ../data/genes_UniProt.fasta -N -m 7" % seq )
    if blastResults[0] != 0:
      out.writeLog("Return code for blast search {} in {} returned with exit code {}!".format( seq, database, blastResults[0] ) )
    return Blast( blastResults[1] )

# if this is the main method, perform some basic tests
if __name__ == "__main__":
  Blast.localBlast()
