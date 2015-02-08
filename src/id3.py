#!/usr/bin/env python
""" 
id3.py is a part of the CS529 Machine Learning project
1 submission for Aaron Gonzales.
It provides functionality for building the actual decision tree
"""
import math
from feature import feature, Leaf
from dna import DNA
from pprint import pprint
# graph tool
import networkx as nx
from metrics import *
from Queue import Queue

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"
__status__ = "Development"
__version__ = "0.1"
__date__ = "2015-01-20"


def build_tree(dna_data):
  """
    Main function for building the tree. Recursively builds going top down
    Args:
      parent_data (list): DNA data, name, sequence, class label
      rootnode_id: id for , may not need this
    Return (Graph): Networkx Graph object that is complete.
  """
  tree = nx.DiGraph()

  ref_data = dna_data
  subfeature_list = []
  # print '********* building root node **********'
  # builds the first node in the tree
  for i in range(0, 57): # hardcoded; whatever
    count_occurances(dna_data, i, subfeature_list)
  # rebuilds subfeature info gain
  for f in subfeature_list:
    info_gain(f)

    # gets the max value for information gain 
  gain_list = [f.info_gain for f in subfeature_list]
    # print 'highest info gain: %f, lowest IG: %f' % (max(gain_list), min(gain_list))
  maxgain_id = gain_list.index(max(gain_list))
  root_f = subfeature_list[maxgain_id]
    # give this feature the data it has to potentially split on
  root_f.data = dna_data
    # make root node
  tree.add_node(root_f, lab=root_f.index)
  parent_f = root_f
  q = Queue()
  q.put(parent_f)

  i = 0
  # i'm so dumb why didn't i put the nodes in a queue

  while q.empty() == False:
    print "Build_Tree: parent_f is %s " % str(parent_f)
    parent_f = q.get()

    # returns a dict with base data
    base_data = make_subclass_vec(parent_f)
    # makde children, a,c,g,t
    # basically have to decide if the node will be a new internal node or a
    # leaf accept state
    for base in base_data.iteritems():
        # this base is a tuple (basepair, data)
        yes, label = check_if_same_class(base)
        if yes is True:
          # this might be an issue with non-uniqe nodes
          # tree.add_node(label + str(yes) + base[0], lab=label)
          leaf = Leaf(label, base)
          tree.add_node(leaf, lab = leaf.label)
          # tree.add_edge(parent_f, label + str(yes) + base[0], base=base[0])
          tree.add_edge(parent_f, leaf, base=base[0])
          continue


        child_f = build_feature(parent_f, base[1])
        # need to check for all pos and neg and if so, label it aas such
        # and call it a leaf node
        if child_f.pos == 0:
          #child_f.leaf_label = '-'
          leaf = Leaf('-', child_f)
          # we have a node with all neg promoters. mark it as such
          tree.add_node(leaf, lab = '-' + str(child_f.index) )
          tree.add_edge(parent_f, leaf, base=base[0] )
          continue
        if child_f.neg == 0:
          # we have a node with all positive promoters. mark it as such
          leaf = Leaf('-', child_f)
          #child_f.leaf_label = '+'
          tree.add_node(leaf, lab = '+'+ str(child_f.index) )
          tree.add_edge(parent_f, child_f, base=base[0] )
          continue

        # if child_f.leaf_label == False: # not a leaf
        #   # test that little dude
        if chi_squared(child_f) == True:
          # add it as a node and base on it
          tree.add_node(child_f, lab = child_f.index)
          tree.add_edge(parent_f, child_f, base=base[0])
          q.put(child_f)
        else:
          leaf = Leaf('x', child_f)
          tree.add_node(leaf, lab = leaf.label)
          tree.add_edge(parent_f, leaf, base=base[0])
          # skip this potential featu. examine this and ensure that it is correct


    print "there are now %d nodes in the tree " % nx.number_of_nodes(tree)
    pprint ( dict([(n,d) for n,d in tree.nodes(data=True)] ))
      #there must be four children here
    #update the parent_f for next layer
    #if tree.successors(parent_f.index) == []:
    # evaluate the node's info gain
    # parent_f = child_f
    # i += 1
  # clean_tree(tree)
  return tree


def check_if_same_class(base):
  """
    Returns if the classes in the data split are all the same or not.
    convenience function
  """
  pos = [p for p in base[1] if p.promoter is True]
  neg = [p for p in base[1] if p.promoter is False]

  if len(pos) == (len(pos) + len(neg)):
    return (True, '+')
  elif len(neg) == (len(pos) + len(neg)):
    return (True, '-')
  else:
    #len(pos) == (len(pos) + len(neg))
    return (False, 'a')


def build_feature(parent_f, base):
  """ build_feature provides functionality for building a node in the tree.
    it's a helper function for build_tree, making the recursion a bit easier.
    Args:
      f (feature): feature we are baseting
  """
  subfeature_list = []
  if len(base) >= 1:
    print ('Build feature: Attempting to build a node from %d values' %
          len(base))
    for i,item in enumerate(base[0].sequence):
      count_occurances(base, i, subfeature_list)
  else:
    # be wary of this
    return None

  # rebuilds subfeature info gain
  for f in subfeature_list:
    info_gain(f)

  if len(subfeature_list) is not 57:
    raise ValueError('check the list being made in build_feature')

  # gets the max value for information gain
  gain_list = [f.info_gain for f in subfeature_list]
  # print 'highest info gain: %f, lowest IG: %f' % (max(gain_list), min(gain_list))
  maxgain_id = gain_list.index(max(gain_list))
  max_f = subfeature_list[maxgain_id]
  # give this feature the data it has to potentially base on
  # print 'assignging data to new max feature'
  # pprint (base)
  max_f.data = base

  return max_f

  # if gain_list[maxgain_id] <= 0.2:
  #   print "Node is not good enough to add"
  #   return None


def make_subclass_vec(f):
  """
  Will make a subclass of features for splitting the data.
  Args:
    data (list): dna objects with feature and labels on them
    feature_index (int): index of the feature we want to split on
  Return:
    sub_data (dict): dict of lists, one for each base 
  """
  # take items in base subclasses of graph's root
  # need to partition data based on a,c,t,g so, get unique instances

  # dna object where feature at feature index is an 'a'
  data = f.data
  feature_index = f.index
  sub_data = {
    'a' : [ pro for pro in data if pro.features[feature_index] is 'a' ],
    'c' : [ pro for pro in data if pro.features[feature_index] is 'c' ],
    'g' : [ pro for pro in data if pro.features[feature_index] is 'g' ],
    't' : [ pro for pro in data if pro.features[feature_index] is 't' ]
  }
  # sub_data = [ a_sub, c_sub, g_sub, t_sub ]
  # print "Made four subclass datasets; here they are"
  f_subvec = []

  # print sub_data
  # for val in sub_data.iteritems():
    # print len(val[1])
    # print val
  return sub_data

def count_occurances(data, feature_index, feature_vec):
  """ 
    Main method to count the instances of occurance at each feature. 
    Builds a feature object.
    data
    Args:
      data (list): list of bases (column vector)
      feature_index: annoying index for getting the right vector
      feature_vec: list that holds all feature objects
    Returns:
      none
  """
  # build pos and neg lists with just the individual base 
  pos = [pro.features[feature_index] for pro in data if pro.promoter is True]
  neg = [ pro.features[feature_index] for pro in data if pro.promoter is False]

  # get base type totals and make a feature object
  base_a = (pos.count('a'), neg.count('a'), pos.count('a') + neg.count('a'))
  base_c = (pos.count('c'), neg.count('c'), pos.count('c') + neg.count('c'))
  base_g = (pos.count('g'), neg.count('g'), pos.count('g') + neg.count('g'))
  base_t = (pos.count('t'), neg.count('t'), pos.count('t') + neg.count('t'))

  f =  feature(len(pos) + len(neg), base_a, base_c, base_g, base_t, len(pos),
               len(neg), feature_index)
  feature_vec.append(f)


def bfs(g, source, dna):
  """ traversal of the tree to find classification
  Args:
    g (networkx) graph: the decision tree
    source (root node):
    dna (DNA): the sequence to classify
  """

  queue = deque([(None, source)])
  enqueued = set([source])
  while queue:
    parent,n = queue.popleft()
    yield parent,n
    new = set(g[n]) - enqueued
    enqueued = new
    queue.extend([(n, child) for child in new])

