#!/usr/bin/env python
""" 
id3.py is a part of the CS529 Machine Learning project
1 submission for Aaron Gonzales.
It provides functionality for building the actual decision tree
"""
import math
from feature import feature
from dna import DNA
from pprint import pprint
# graph tool
import networkx as nx
from metrics import *

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
  DEBUG = True
  # empty graph object
  id3_tree = nx.DiGraph()

  ref_data = dna_data
  subfeature_list = []
  print '********* building root node **********'
  # builds the first node in the tree
  for i in range(0, 57): # hardcoded; whatever
    count_occurances(dna_data, i, subfeature_list)

  # rebuilds subfeature info gain
  for f in subfeature_list:
    info_gain(f)

  # gets the max value for information gain 
  gain_list = [f.info_gain for f in subfeature_list]
  print 'highest info gain: %f, lowest IG: %f' % (max(gain_list), min(gain_list))
  maxgain_id = gain_list.index(max(gain_list))
  root_f = subfeature_list[maxgain_id]
  # give this feature the data it has to potentially split on
  root_f.data = dna_data

  # make root node
  id3_tree.add_node(root_f.index, data=root_f)
  parent_f = root_f
  print "Should just be root node: %s " % id3_tree.nodes()

  # networkx search by 
  # everything is a dict of dicts and so on
  # so each node has a simple key
  # and optional value, which is a dict
  # example goes like this, getting the nodes with data = nums ( alist)
  # a = g.nodes(data=nums)
  # a[0][1]['data']
  # e.g. first node, first list, first key

  i = 0
  # continue building when misclassj
  while i < 4:
    print "Build_Tree: parent_f is %d " % parent_f.index
    # print "Build_Tree: parent_f node's size is %d " % print_node(id3_tree,
        # parent_f)
    # set pointer to the parent_f node's data
    # parent_f = id3_tree.node[parent_f]
    print "build: type of parent_f: %s" % type(parent_f)

    # returns a dict with split data
    split_data = make_subclass_vec(parent_f)
    print "Build_Tree while: split_data is of type %s " % type(split_data)
    pprint (split_data)

    split_length = [ len(split[1]) for split in split_data.iteritems() ] 

    for split in split_data.iteritems():
      # this split is a tuple (key, val)
      if len(split[1]) < 2:
        # stop and make me a leaf, skip to next
        print "data too small to split; making leaf"
        id3_tree.add_node('leaf' + split[0])
        id3_tree.add_edge(parent_f.index, 'leaf' + split[0]) 
        continue

      # pass just the list of dna and index of split
      child_f = build_node(parent_f, split[1])
      if child_f is None:
        print 'node failed to be built'
        id3_tree.add_node('+/-', data=['leaf'])
        id3_tree.add_edge(parent_f, '+/-')
        continue
      else:
        id3_tree.add_node(child_f.index, data=child_f) # don't forget split tuple
        id3_tree.add_edge(parent_f.index, child_f.index)
    #update the parent_f for next layer
    if child_f is not None:
      parent_f = child_f
    else:
      # get out of loop, all leaves
      break
    i += 1

  print (id3_tree.adjacency_list())
  print id3_tree.nodes()
  print nx.info(id3_tree)
  print nx.adjacency_matrix(id3_tree)
  return id3_tree


def build_node(split_f, split_data):
  """ build_node provides functionality for building a node in the tree.
    it's a helper function for build_tree, making the recursion a bit easier.
    Args:
      f (feature): feature we are splitting
  """
  # print "Build Node: dataset's type is : %s" % type(dataset)
  # print "Build Node: f_split is type : %s" % type(dataset)

  # list of each feature object, with a column vector of chars
  # rebuilds the counts for each type of base
  # i should have used a numpy matrix or something like that for ease.
  subfeature_list = []
  if split_f.index is not None:
    print ('Build Node: Attempting to build a node from %d values' %
          len(split_data))
    for i,item in enumerate(split_data[0].sequence):
      count_occurances(split_data, i, subfeature_list)

  # rebuilds subfeature info gain
  for f in subfeature_list:
    info_gain(f)

  # gets the max value for information gain 
  gain_list = [f.info_gain for f in subfeature_list]
  print 'highest info gain: %f, lowest IG: %f' % (max(gain_list), min(gain_list))
  maxgain_id = gain_list.index(max(gain_list))
  max_f = subfeature_list[maxgain_id]
  # give this feature the data it has to potentially split on
  max_f.data = split_data

  # evaluate the node's info gain
  if gain_list[maxgain_id] <= 0.1:
    print "Node is not good enough to add"
    return None

  return (max_f)

def print_node(g, node_index):
  print 'size of node: '
  #print len(g.node[node_index]['data'])

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
    'a_sub' : [ pro for pro in data if pro.features[feature_index] is 'a' ],
    'c_sub' : [ pro for pro in data if pro.features[feature_index] is 'c' ],
    'g_sub' : [ pro for pro in data if pro.features[feature_index] is 'g' ],
    't_sub' : [ pro for pro in data if pro.features[feature_index] is 't' ]
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
  base_a = (pos.count('a'), neg.count('a'), pos.count('a') + neg.count('a')  )
  base_c = (pos.count('c'), neg.count('c'), pos.count('c') + neg.count('c')  )
  base_g = (pos.count('g'), neg.count('g'), pos.count('g') + neg.count('g')  )
  base_t = (pos.count('t'), neg.count('t'), pos.count('t') + neg.count('t')  )

  f =  feature(len(pos) + len(neg), base_a, base_c, base_g, base_t, len(pos),
               len(neg), feature_index)
  feature_vec.append(f)


