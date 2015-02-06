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
# graph tool
import networkx as nx

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"



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
               len(neg))
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
    entpos = 0
  # print "ent pos: %f" % entneg
  # print "ent neg: %f" % entneg
  ent = entpos + entneg

  # ent = (p_pos * math.log(p_pos, 2) ) - (p_neg * math.log(p_neg, 2))
  # print "entropy: %f " % ent
  return ent


def info_gain(f):
  """ Calculates the information gain for a node
  feature_vec is each value v of all possible values of attribte a
  f_v subset of feature_vec for which attribute a has value v
  |f_v| notation for size of set
  """
  # need to calc info gain for the full feature
  info_f = -(f.pos/f.n * math.log(f.pos/f.n, 2) ) - (f.neg/f.n * math.log(f.neg/f.n, 2))
  print "The set's  information is: %f" % info_f

  info = float(0)
  info_sum = float(0)
  for base in f.bases:
    print 'for loop in info gain: base = %s ' 
    print base, info
    info = base[2]/f.n * entropy(base, f.n)
    info_sum += info
    print 'for loop in info gain: done'
    print base, info, info_sum

  info_gain = info_f - info_sum
  f.info_gain = info_gain



  
def chi_squared(p, n, counts, prob, pcount):
  """
  Performs the chi-squared test needed for testing effectiveness of a split.
  """
    

def build_tree():
  """
    class here for the DNA object
    that should include the classification (promoter / not), 
    instance name, and sequence as fields in the object
    main will create objects when ran
  """
  #From data mining book
#    create a node N ;
#    if tuples in D are all of the same class, C:
#      return N as a leaf node labeled with the class C;
#    if attribute list is empty then
#        return N as a leaf node labeled with the majority class in D; # majority voting
#    apply Attribute selection method(D, attribute list) to find the "best" splitting criterion;
#    label node N with splitting criterion;
#    if splitting attribute is discrete-valued and multiway splits allowed then # not restricted to binary trees
#      attribute list = attribute list - splitting attribute; # remove splitting attribute
#    for each outcome j of splitting criterion:
#      # partition the tuples and grow subtrees for each partition
#      let D j be the set of data tuples in D satisfying outcome j; # a partition
#        if D j is empty: 
#          attach a leaf labeled with the majority class in D to node N ;
#        else attach the node returned by Generate decision tree(D j , attribute list) to node N ;
#    endfor
#    return N 
  return None


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = "DNA Promoter ID3 classifer")
  parser.add_argument("filename", 
      help = 'the DNA promoter data file')
  args = parser.parse_args()

  data = []
  data_dict = dict()
  # read the file 
  with open(args.filename, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for line in f:
      # strips all whitespace within fields, including tabs and newlines without seperators 
      # as the file is full of weird extra spaces and such
      gene = [field.strip() for field in line.split(',')]
      dna = DNA(gene[0],gene[1],gene[2])
      # slow way of growing a list but it works for this purpose
      data.append(dna)
      data_dict[dna.name] = (dna.promoter, dna.features)


  print "Size of test: %d" % len(data)
  print "Size of testdict: %d" % len(data_dict)

  # count = count_occurances(data, 1)
  # print "Count: pos: %s; neg: %s " % count

  # convenience 
  seq_length = len(data[0].features)

  # caculate the total pos/neg occurances for each feature in the set
  total_counts = {}
  feature_list = []
  for i in range(0, seq_length):
    total_counts[i] = count_occurances(data, i, feature_list)

  # from pprint import pprint
  # print "Total initial counts for occurances"
  # pprint (total_counts)

  print "doing info gain for a feature"
  Info_D = info_gain(feature_list[0])
  for f in feature_list:
    info_gain(f)

  # print "Information gain for all attributes: %f" % Info_D

  

