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
  pos = [pro.features[feature_index] for pro in data if pro.promoter == True]
  neg = [ pro.features[feature_index] for pro in data if pro.promoter == False]

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


def build_node():
  """ Method for building a node in the parse tree.
  requires entropy, info_gain, and the set of current attributes
  """



def entropy(base, n):
  """ Calculates the entropy of a set of attributes
  Attributes:
    base - Feature
  """
  # convenience

  # base case, need to chekc this
  # if base[2] <=1  or base[0]  <=1 or base[1]  <= 1:
  if base[2] <=1: 
    return 0

  p_pos = base[0]/base[2]
  p_neg = base[1]/base[2]
  # print math.log(p, 2)
  # print "p pos: %f" % p_pos
  # print "p neg: %f" % p_neg
  if p_pos != 0:
    entpos = -1* (p_pos * math.log(p_pos, 2) )
  else:
    entpos = 0
  if p_neg != 0:
    entneg = -1* (p_neg * math.log(p_neg, 2) )
  else:
    entneg = 0
  # print "ent pos: %f" % entneg
  # print "ent neg: %f" % entneg
  ent = entpos + entneg

  # ent = (p_pos * math.log(p_pos, 2) ) - (p_neg * math.log(p_neg, 2))
  # print "entropy: %f " % ent
  return ent


def info_gain(f):
  """ Calculates the information gain for a node
  Args:
  f (Feature): a feature
  """
  DEBUG = False
  # check for empty values
  if 0 in [f.pos, f.n, f.neg]:
    f.info_gain = 0
    return

  # need to calc info gain for the full feature
  info_f = -(f.pos/f.n * math.log(f.pos/f.n, 2) ) - (f.neg/f.n * math.log(f.neg/f.n, 2))
  if DEBUG:
    print "The set's  information is: %f" % info_f

  info = float(0)
  info_sum = float(0)
  for base in f.bases:
    info = base[2]/f.n * entropy(base, f.n)
    info_sum += info
    if DEBUG: 
      print 'for loop in info gain: done'
      print base, info, info_sum

  info_gain = info_f - info_sum
  f.info_gain = info_gain

  
def chi_squared(f):
  """
  Performs the chi-squared test needed for testing effectiveness of a split.
  """
  # simply, 
  # sum (observed - expected)^2
  #     ------------------------
  #          expected

  # sum  (promoters_ichild - expected_promoters_ichild)^2  + (non-p_i - # exp_non_pi)^2
  #   -----------------------------------------------------  -------------------------
  #       exp_promoters_ichild                                      exp_non_pi
    

def build_tree(parent_data, rootnode_id):
  """
    class here for the DNA object
    that should include the classification (promoter / not), 
    instance name, and sequence as fields in the object
    main will create objects when ran
  """
  DEBUG = True
  print '------starting build_tree '
  if parent_data is None:
    print '------data empty or null'
    return None
  if len(parent_data) <= 1:
    print 'data <= 1'
    # make a leaf?
    return
  # if chi_sq <= 10:
  #   print 'chi_sq is too low'
  #   return None

  # remember, this gives back a dict
  sub_data = make_subclass_vec(parent_data, rootnode_id)
  pprint (sub_data)
  info_vector = [rootnode_id] 
  prev_feats = [rootnode_id]
  feature_dict = {}
  maxgain_id = None

  # main loop
  for dataset in sub_data.itervalues():
    build_tree_helper(dataset, feature_dict, maxgain_id)
                  
  info_vector.append(maxgain_id)
  print info_vector


def build_tree_helper(dataset, feature_dict, maxgain_id):

  print 'Attempting to reclassify %d values' % len(dataset)
  if len(dataset) <= 1:
    print "------passing"
    pass

  pprint (dataset)
  # list of each feature object, with a column vector of chars
  subfeature_list = []

  # rebuilds the counts for each type of base
  for i,item in enumerate(dataset[0].sequence):
    count_occurances(dataset, i, subfeature_list)

  # rebuilds subfeature info gain
  for f in subfeature_list:
    info_gain(f)

  if len(dataset) <= 2:
    for s in subfeature_list:
      print str(s)
  tmp = [f.info_gain for f in subfeature_list]
  print max(tmp), min(tmp)

  # make a dict with each feature's ID
  feature_dict = dict(zip(range(0,57), subfeature_list))
  # pprint (feature_dict)

  # gets the index of the item with largest info gain;may need checking on prev
  # values
  maxgain_id =  max(feature_dict.iterkeys(), key=lambda k: feature_dict[k].info_gain) 

  # recurse
  build_tree(dataset, maxgain_id)


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

  

