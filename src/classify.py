""" 
classify.py searches through the data and gives classifications.
"""
import id3 as id3
import feature
from Queue import Queue

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"


def search_tree(d_tree, root, dna_n):
  """ traversal of the tree to find classification
  Args:
    d_tree (networkx) d_treeraph: the decision tree
    root (root node):
    dna (DNA): the sequence to classify
  """
  print "root node is at index: %d " % root.index

  # testing
  q = Queue()
  q.put(root)
  while q.empty() is False:
    current_node = q.get()
    base = dna_n.base_at_index(current_node.index)
    print ('current node: id: %d,  leaf: %s, label = %s ' %
        (current_node.index, current_node.is_leaf, current_node.label))
    if current_node.is_leaf:
      # print "i'm a leaf and have label of %s " % str(current_node.label)
      return current_node.label
    if current_node.is_leaf is False:
      print 'following the base %s' % base
      # d_treeet the node at the end of the edd_treee in this node/seq pair
      # make the successor edges of the root to test following
      child_edges = [(current_node, node) for node in d_tree.successors(current_node)]
      for u,v in child_edges:
        e =  d_tree.get_edge_data(u,v)
        print e
        print (u.index, v.index)
        # follow the right edge:
        if e['base'] is base:
          q.put(v)
          break


def classify(d_tree, test_data):
  """ gets the accuracy of a given file based on the built decision tree.
  Args:
    d_tree (networkx tree): the built decision tree
    test_data (list) of 
  Return: (list) the results?
  """
  DEBUG = True
  if DEBUG:
    from pprint import pprint
  if test_data is None:
    raise TypeError('The test data is empty')
  root = 0
  # can't use list comp with error checking, since networkx has multiple things
  # as node types
  for node in d_tree.nodes():
    try:
      if node.is_root is True:
        root = node
    except AttributeError:
      # print ("found a leaf")
      continue
  # print 'got a root node at index: %d' %root.index
  # # label = search_tree(d_tree, root, test_data)
  # finished_data = [(d.promoter, search_tree(d_tree,root,d)) for d in test_data]
  labels = [ '+' == search_tree(d_tree,root,d) for d in test_data]
  pprint(labels)
  promoters = [p.promoter for p in test_data]
  finished = [(p,l,p == l) for p,l in zip(promoters, labels)]
  pprint (finished)


def get_error(label_set):
  """ Gets the error rate / confusion matrix for the classification
  Args:
    label_set (bool, bool, bool): 3-tuple of a sample's (real_promoter,
    assigned_promoter, correct)
  """


