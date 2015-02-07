#!/usr/bin/env python
""" 
main.py is the primary file that runs the decsion tree parser

"""

import sys
import argparse
import id3
import process_data
import math
from feature import feature
from dna import DNA
from id3 import *
import os
from pprint import pprint
import networkx as nx
from metrics import *
import process_data
import matplotlib as plt
import pygraphviz as pgv
__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"



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
  read_file(data, args)

  print "Size of the read data: %d" % len(data)

  tree = build_tree(data)
  graph = nx.to_agraph(tree)
  print graph
  graph.layout()
  graph.draw('test_clas.png')


  try:
    from networkx import graphviz_layout
  except ImportError:
    raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")

  pos=nx.graphviz_layout(tree,prog='twopi',args='')
  nx.draw(graph,pos,node_size=20,alpha=0.5,node_color="blue", with_labels=False)
  plt.axis('equal')
  plt.savefig('circular_tree.png')
  plt.show()




  ## cross validate?
  ## train
  ## test

