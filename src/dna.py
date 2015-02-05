
__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"
__status__ = "Development"


class DNA(object):
  """ Main class for DNA objects.
  Holds relevent information about the dna, including promoter type, name, and
  sequence. convenience methods for getting information and sorting?

  Attributes:
    promoter: One of {+/-}, indicating the class ("+" = promoter).
    name:   The instance name (non-promoters named by position in the 1500-long
            nucleotide sequence provided by T. Record).  
    sequence: The remaining 57 fields are the sequence, starting at 
         position -50 (p-50) and ending at position +7 (p7). Each of
         these fields is filled by one of {a, g, t, c}.
    features: Dictionary of the above sequence.
    """
  def __init__(self, promoter, name, sequence):
    self.name = name
    self.sequence = list(sequence)
    if promoter is '+':
      self.promoter = True
    else:
      self.promoter = False

    # make a dict with key of feature number and val of the base
    index = range(0, len(sequence))
    self.features = {}
    for index, feature in zip(index, sequence):
      self.features[index] = feature


  def get_info(self):
    print " -- Debug: DNA object name class: %s " % self.name
    print " -- Debug: DNA object promoter class: %s " % self.promoter
    print " -- Debug: DNA object sequence class: %s " % self.sequence
    print " -- Debug: DNA object features class: %s " % self.features
