#!/usr/bin/env python
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



def count_occurances(data, feature_index):
  """ 
    Main method to count the instances of occurance at each feature. 
    Builds two key dictionaries that keep track of counts for each dna base in a
    feature for further processing. 
  """
  # build pos and neg lists with just the individual base 
  pos = [pro.features[feature_index] for pro in data if pro.promoter == True]
  neg = [ pro.features[feature_index] for pro in data if pro.promoter == False]

  # debugging
  # print "Positive length: %d" % len(pos)
  # print "Negative length: %d" % len(neg)
  count = (len(pos), len(neg))

  # get base type totals for pos and neg sets
  pos_totals = { 
      'a':pos.count('a'),
      'c':pos.count('c'),
      'g':pos.count('g'),
      't':pos.count('t'),
      'count': len(pos)
      }  
  neg_totals = { 
      'a':neg.count('a'),
      'c':neg.count('c'),
      'g':neg.count('g'),
      't':neg.count('t'),
      'count': len(neg)
      }  
  # print 'Positive Totals: %s ' % pos_totals
  # print 'Negative Totals: %s ' % neg_totals

  return (pos_totals, neg_totals)


def build_node():
  """ Method for building a node in the parse tree.
  requires entropy, info_gain, and the set of current attributes
  """



def entropy(feature):
  """ Calculates the entropy of a set of attributes
  where S is the set and p the proportion of S beloning to class I. is 
  """
  # convenience
  n = len(feature)

  # base case
  if n <= 1:
    return 0

  for p in probability:
    entropy -= p * log(p, base=2)

  return entropy


def info_gain(feature):
  """ Calculates the information gain for a node
  feature is each value v of all possible values of attribte a
  f_v subset of feature for which attribute a has value v
  |f_v| notation for size of set
  """
  print feature
  # print feature[0].get('a')
  a = feature[0].get('a') / feature[1].get('a')
  c = feature[0].get('c') / feature[1].get('c')
  g = feature[0].get('g') / feature[1].get('g')
  t = feature[0].get('t') / feature[1].get('t')



  
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
  for i in range(0, seq_length):
    total_counts[i] = count_occurances(data, i)

  from pprint import pprint
  print "Total initial counts for occurances"
  pprint (total_counts)

  print "doing info gain for a feature"
  info_gain(total_counts[1])

  

