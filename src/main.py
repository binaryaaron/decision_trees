#!/usr/bin/env python
""" 
main.py is the primary file that runs the decsion tree parser

"""
import sys
import argparse
import os
import csv
import id3

from feature import feature
from dna import DNA
import classify as classify

# from pprint import pprint

# graph tool
try:
  import networkx as nx
  from networkx import graphviz_layout
  import pygraphviz as pgv
  import matplotlib.pyplot as plt
except ImportError:
  raise ImportError("This program requires Graphviz, pygraphviz, networkx, and matplotlib")


__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"


def read_file(data_list, filename):
  with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=' ')
    for line in f:
      # strips all whitespace within fields, including tabs and newlines without seperators 
      # as the file is full of weird extra spaces and such
      gene = [field.strip() for field in line.split(' ')]
      dna = DNA(gene[0],gene[1])
      # slow way of growing a list but it works for this purpose
      data_list.append(dna)


def draw_tree(tree):
  # make new labels for edges:
  # from pprint import pprint

  # fun way to get the labels correct for the edges instead of having
  # the damn kev, val pair printed by default
  # this returns the attributes in a dict for the right key, 'base'
  # and that's passed directly into draw_networkx_edge_labels
  edge_att = nx.get_edge_attributes(tree, 'base')

  # pprint ( dict([(n,d['lab']) for n,d in tree.nodes(data=True)] ))
  node_labels=dict((n,d['lab']) for n,d in tree.nodes(data=True))
  # pprint(node_labels)

  nx.relabel_nodes(tree,node_labels)
  pos=nx.graphviz_layout(tree, prog='dot')
  # pos=nx.spring_layout(tree, iterations=1000, scale=2)

  nx.draw_networkx_nodes(tree, pos, node_size = 1000)
  nx.draw_networkx_labels(tree, pos, labels=node_labels, node_size = 1000)
  nx.draw_networkx_edges(tree, pos, node_size = 1000)
  nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_att)



  # nx.draw(tree, pos, with_labels=True, node_size = 1000)

  plt.title("ID3 tree")
  plt.savefig('decision_tree.png')
  nx.write_dot(tree, 'decision_tree.dot')

  # thesting
  order =  nx.topological_sort(tree)
  print "topological sort"
  print [str(node.index) for node in order]

def main(args):
  data = []
  # read the file 
  read_file(data, args.filename)
  tree = id3.build_tree(data)
  draw_tree(tree)
  train_data = []
  train_file = '../data/validation.txt'
  read_file(train_data, train_file)
  classify.classify(tree, data)

  print 'goodbye'

if __name__ == "__main__":
  # gotta parse those args
  parser = argparse.ArgumentParser(description = "DNA Promoter Decision Tree maker thingy")
  parser.add_argument("filename", 
      help = 'the DNA promoter data file')
  parser.add_argument("metric",
      help = 'the metric you want to use, ID3 or MCE')
  args = parser.parse_args()
  main(args)




