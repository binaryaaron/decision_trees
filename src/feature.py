__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"
__status__ = "Development"


class feature(object):
  """ 
  Holds state information about a feature.
  Args:
    n : size of the feature
    a : tuple of base pair a (n_pos, n_neg, n_tot)
    c : tuple of base pair c (n_pos, n_neg, n_tot)
    g : tuple of base pair g (n_pos, n_neg, n_tot)
    t : tuple of base pair t (n_pos, n_neg, n_tot)
    pos : number of positive features
    neg : number of negative features
    index : this feature's place

  Attributes:
    bases : tuple of the bases a,c,g,t
    info : information for this feature
    info_gain : information gained by splitting on this feature
  """
  def __init__(self, n,a,c,g,t, pos, neg, index):
    # total size of feature
    self.n = n
    # tuples for each base
    self.a = a
    self.c = c
    self.g = g
    self.t = t
    self.bases = (a,c,t,g)
    self.pos = pos
    self.neg = neg
    self.info = float(-10)
    self.info_gain = float(-10)
    self.index = index

  def print_me(self):
    print " -- Debug: feature object bases = " 
    print self.bases
    print " -- Debug: feature object size = %d "  % self.n
    print " -- Debug: feature object info_gain = %f " % self.info_gain
