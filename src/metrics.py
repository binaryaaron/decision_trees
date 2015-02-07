#!/usr/bin/env python
from __future__ import division
""" 
process_data.py is the helper file that will read DNA promoter data
and create objects from that. It is a part of the CS529 Machine Learning project
1 submission for Aaron Gonzales.
"""

import math
from pprint import pprint

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"


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

  
def chi_squared(f, threshold=95):
  """
  Performs the chi-squared test needed for testing effectiveness of a split.
  """
  # sum  (promoters_ichild - expected_promoters_ichild)^2  + (non-p_i - # exp_non_pi)^2
  #   -----------------------------------------------------  -------------------------
  #       exp_promoters_ichild                                      exp_non_pi
    # feature reference
    # n : size of the feature
    # a : tuple of base pair a (n_pos, n_neg, n_tot)
    # recall that a base is a 4tuple with 
  chisq = float(0)
  # degrees of freedom vary if a base is empty
  dof = 3
  # little dictionary of mins
  chisq_mins = {
      95 : {
        1 : 3.841,
        2 : 5.991,
        3 : 9.837,
        4 : 11.668
        }, 
      99 : {
        1 : 6.635,
        2 : 9.210,
        3 : 11.345,
        4 : 13.227 
        }
      }

  print str(f)
  for base in f.bases:
    base_pos = base[ 0 ]
    base_neg = base[ 1 ]
    base_tot = base[ 2 ]
    print ' this base is : %s ' % str(base)
    if base_tot == 0:
      dof -= 1
      continue
    expected_pos = base_tot * (f.pos/f.n)
    expected_neg = base_tot * (f.neg/f.n)
    chi_pos =((base_pos - expected_pos)**2) / expected_pos
    chi_neg = ((base_neg - expected_neg)**2) / expected_neg
    chisq += chi_pos + chi_neg
  print ("chi_squared minium value for dof: %d and threshold %d: %f " %
      (dof, threshold, chisq_mins[threshold][dof]) )
  print "computed chi_squared value : %d" % chisq

  return chisq > chisq_mins[threshold][dof]







