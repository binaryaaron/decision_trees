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
    self.is_root = False
    self.is_leaf = False
    self.label = 'feature'
    if self.index == None:
     raise AttributeError("this feature is missing an index somewhere")

  def __str__(self):
    """ Makes a pseudo-hash out of its items
    this is entirely for NetowrkX's drawing of the tree, due to some weird
    issue with GraphViz formats. GraphViz will not have duplicatly labeled
    nodes, even though they theyselves are unique.
    NetworkX uses the __str__ override to print
    """
    return str(self.index * self.n * self.pos)

class Leaf(object):
  """
  convenience class for a leaf node in the tree.
  Args:
    label (str): the classification label
    data (list): potentially useful holder, may remove
  Attributes :
    is_leaf :  helper for drawing and searching through the completed tree, as
              NetworkX is wonky about searching for keys and values that are
              not similar in all the  graph.
  """

  def __init__(self, label, data):
    self.label = label
    self.data = data
    self.is_leaf = True
    self.index = -1

  def __str__(self):
    """ Makes a pseudo-hash out of its items
    this is entirely for NetowrkX's drawing of the tree, due to some weird
    issue with GraphViz formats. GraphViz will not have duplicatly labeled
    nodes, even though they theyselves are unique.
    NetworkX uses the __str__ override to print
    """
    return str(hash(self))
