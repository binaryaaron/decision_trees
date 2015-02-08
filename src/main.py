#!/usr/bin/env python
""" 
main.py is the primary file that runs the decsion tree parser

"""
import id3
from feature import feature
from dna import DNA

import sys
import argparse
import os
import csv
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
  # TODO need to modify this to fit the new data  file from LEARN not UCI
  with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=' ')
    for line in f:
      # strips all whitespace within fields, including tabs and newlines without seperators 
      # as the file is full of weird extra spaces and such
      gene = [field.strip() for field in line.split(' ')]
      print gene
      dna = DNA(gene[0],gene[1])
      # slow way of growing a list but it works for this purpose
      data_list.append(dna)

if __name__ == "__main__":
  # gotta parse those args
  parser = argparse.ArgumentParser(description = "DNA Promoter Decision Tree maker thingy")
  parser.add_argument("filename", 
      help = 'the DNA promoter data file')
  parser.add_argument("metric",
      help = 'the metric you want to use, ID3 or MCE')
  args = parser.parse_args()

  data = []
  # read the file 
  read_file(data, args.filename)

  print "Size of the read data: %d" % len(data)

  tree = id3.build_tree(data)
  # print (tree.adjacency_list())
  # print tree.nodes()
  # print nx.info(tree)
  # print nx.adjacency_matrix(tree)
  graph = nx.to_agraph(tree)
  # print graph
  graph.layout()
  graph.draw('test_clas.png')

  plt.title("draw_networkx")
  pos=nx.graphviz_layout(tree,root = 16, prog='dot')
  nx.draw(tree,pos,with_labels=True, node_size = 1000)
  nx.draw_networkx_edge_labels(tree,pos)
  plt.savefig('nx_test.png')
  nx.write_dot(tree, 'decision_tree.dot')



  ## cross validate?
  ## train
  ## test

