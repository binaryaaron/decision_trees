#!/usr/bin/env python
""" 
It is a part of the CS529 Machine Learning project
1 submission for Aaron Gonzales.
"""

import sys
import argparse
import csv 
import id3
import process_data

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"
__status__ = "Development"
__version__ = "0.1"
__date__ = "2015-01-20"


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


def build_node():
  """ Method for building a node in the parse tree.
  requires entropy, info_gain, and the set of current attributes
  """
