#!/usr/bin/env python
""" 
id3.py is a part of the CS529 Machine Learning project
1 submission for Aaron Gonzales.
It provides functionality for building the actual decision tree
"""

import sys
import argparse
import csv 
import id3
import process_data
import networkx as nx
from process_data import *
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
  id3_tree = nx.Graph()

  build = True
  ref_data = dna_data
  print '********* building root node **********'
  root_node = build_node(dna_data, None)
  # make root node
  id3_tree.add_node(root_node.index, data=ref_data)
  parent_index = root_node.index
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
  while i < 4:
    print "Build_Tree: parent_index is %d " % parent_index
    print_node(id3_tree, parent_index)
    # print "Build_Tree: parent_index node's size is %d " % print_node(id3_tree,
        # parent_index)
    # set pointer to the parent_index node's data
    p_data = id3_tree.node[parent_index]['data']
    print "build: type of p_data: %s" % type(p_data)

    # returns a dict with split data
    split_data = make_subclass_vec(p_data, parent_index)
    # print "Build_Tree while: split_data is of type %s " % type(split_data)

    split_length = [ len(split[1]) for split in split_data.iteritems() ] 

    for split in split_data.iteritems():
      # this split is a tuple (key, val)
      if len(split[1]) < 2:
        # stop and make me a leaf, skip to next
        print "data too small to split; making leaf"
        id3_tree.add_node('+/-')
        id3_tree.add_edge(parent_index, '+/-')
        break

      # pass just the list of dna and index of split
      child = build_node(split[1], parent_index)
      if child is None:
        print 'node failed to be built'
        id3_tree.add_node('+/-', data=['leaf'])
        id3_tree.add_edge(parent_index, '+/-')
        pass
      else:
        id3_tree.add_node(child.index, data=split[1]) # don't forget slit tuple
        id3_tree.add_edge(parent_index, child.index)
        parent_index = child.index
    i += 1

  print (id3_tree.adjacency_list())
  print id3_tree.nodes()
  print nx.info(id3_tree)
  print nx.adjacency_matrix(id3_tree)
  return id3_tree


def build_node(dataset, f_split):
  """ build_node provides functionality for building a node in the tree.
    it's a helper function for build_tree, making the recursion a bit easier.
    Args:
      dataset (list): of dna objects
      f_split (int): index of the thing on which we are splitting
  """
  # print "Build Node: dataset's type is : %s" % type(dataset)
  # print "Build Node: f_split is type : %s" % type(dataset)

  # list of each feature object, with a column vector of chars
  # rebuilds the counts for each type of base
  # i should have used a numpy matrix or something like that for ease.
  subfeature_list = []
  if f_split is not None:
    print 'Build Node: Attempting to build a node from %d values' % len(dataset)
    for i,item in enumerate(dataset[0].sequence):
      count_occurances(dataset, i, subfeature_list)
  else:
    # builds the first node in the tree
    print 'Build Node: Attempting to build a node from %d values' % len(dataset)
    for i in range(0, 57): # hardcoded; whatever
      count_occurances(dataset, i, subfeature_list)

  # rebuilds subfeature info gain
  for f in subfeature_list:
    info_gain(f)

  # gets the max value for information gain 
  gain_list = [f.info_gain for f in subfeature_list]
  print 'highest info gain: %f, lowest IG: %f' % (max(gain_list), min(gain_list))
  maxgain_id = gain_list.index(max(gain_list))
  max_f = subfeature_list[maxgain_id]

  # evaluate the node's info gain
  if gain_list[maxgain_id] <= 0.1:
    print "Node is not good enough to add"
    return None

  return (max_f)

def print_node(g, node_index):
  print 'size of node: '
  #print len(g.node[node_index]['data'])

