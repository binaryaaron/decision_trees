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
    data (list): the data that will be present for a if we split upon it. 
                e.g., if we split on feature f, f.data = subset of data indexed
                by that feature.
    leaf_label ( string): label if this is a leaf node.
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
    self.data = None
    self.leaf_label = False

  def __str__(self):
    return (
        "<Feature Obj: \n ----n = " + str(self.n) +
        "\n----bases: '" + str(self.bases) +
        "\n----info_gain: "  + str(self.info_gain )+
        "\n----self.pos: " + str(self.pos) +
        "\n----self.neg: " + str(self.neg)
        )
