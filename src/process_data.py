#!/usr/bin/env python
from __future__ import division
""" 
process_data.py is the helper file that will read DNA promoter data
and create objects from that. It is a part of the CS529 Machine Learning project
1 submission for Aaron Gonzales.
"""

import sys
import argparse
import csv 
import id3
import process_data
import math
from feature import feature
from dna import DNA
from id3 import *
import os
from pylab import *
from collections import Counter
from pprint import pprint
# graph tool
import networkx as nx

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"


def make_subclass_vec(data, feature_index):
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
  # f.get_info()
  # return (pos_totals, neg_totals)






##### Do the thing ######
if __name__ == "__main__":
  # gotta parse those args
  parser = argparse.ArgumentParser(description = "DNA Promoter ID3 classifer")
  parser.add_argument("filename", 
      help = 'the DNA promoter data file')
  args = parser.parse_args()

  data = []
  # read the file 
  # TODO need to modify this to fit the new data  file from LEARN not UCI
  with open(args.filename, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for line in f:
      # strips all whitespace within fields, including tabs and newlines without seperators 
      # as the file is full of weird extra spaces and such
      gene = [field.strip() for field in line.split(',')]
      dna = DNA(gene[0],gene[1],gene[2])
      # slow way of growing a list but it works for this purpose
      data.append(dna)

  print "Size of the read data: %d" % len(data)

  # convenience for length of a feature
  seq_length = len(data[0].features)

  # list of each feature object, with a column vector of chars
  feature_list = []
  for i in range(0, seq_length):
    count_occurances(data, i, feature_list)

  for f in feature_list:
    info_gain(f)

  # tmp = [f.info_gain for f in feature_list]
  # print max(tmp), min(tmp)

  # make a dict with each feature's ID
  feature_dict = dict(zip(range(0,seq_length), feature_list))

  # gets the index of the item with largest info gain
  rootnode_id = max(feature_dict.iterkeys(), key=lambda k: feature_dict[k].info_gain)
  print "Highest information gain found was %f at feature id: %d" % (feature_dict[rootnode_id].info_gain, rootnode_id)
  id3_tree = nx.Graph()
  id3_tree.add_node(rootnode_id, feature=feature_dict[rootnode_id]) 
  print id3_tree.nodes()
  id3_tree.add_node(3, feature=feature_dict[3])
  id3_tree.add_edge(rootnode_id, 3)
  print id3_tree.nodes()
  print id3_tree.edges()

  build_tree(data, rootnode_id)

  

  # i need a way to get dna and feature index pos





  # print "Information gain for all attributes: %f" % Info_D

  

