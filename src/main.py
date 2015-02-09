#!/usr/bin/env python
"""
main.py is the primary file that runs the decsion tree program
and draws the output.
"""
import sys
import argparse
import os
import csv
from pprint import pprint

import id3
from feature import feature
from dna import DNA
import classify as classify

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
  """ Reads a file with DNA promoter data
      and fills a list with that data.
      Args:
        data_list (list) : the empty list you want to put data into
        filename (str) : path to the file you want to open
  """
  with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=' ')
    for line in f:
      # splits the line into the part with the promoter and the sequence for easy
      # processing
      gene = [field.strip() for field in line.split(' ')]
      dna = DNA(gene[0],gene[1])
      # slow way of growing a list but it works for this purpose
      data_list.append(dna)


def draw_tree(tree, conf):
  """ Draws the tree to a png file using NetworkX, Matplotlib, and GraphViz
  """
  # fun way to get the labels correct for the edges instead of having
  # the damn kev, val pair printed by default
  # this returns the attributes in a dict for the right key, 'base'
  # and that's passed directly into draw_networkx_edge_labels
  edge_att = nx.get_edge_attributes(tree, 'base')

  node_labels=dict((n,d['lab']) for n,d in tree.nodes(data=True))
  # pprint(node_labels)

  nx.relabel_nodes(tree,node_labels)
  # dot layout required for a tree and only available in graphviz_layout form
  pos=nx.graphviz_layout(tree, prog='dot')

  nx.draw_networkx_nodes(tree, pos, node_size = 1000)
  nx.draw_networkx_labels(tree, pos, labels=node_labels )
  nx.draw_networkx_edges(tree, pos, node_size = 1000)
  nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_att)

  plt.axis('off')
  plt.title("Decision Tree for DNA Promoter Data; " + conf + "% confidence")
  plt.savefig('decision_tree.pdf')


def main(parser):
  """ Drives the program.
  """
  args = parser.parse_args()
  if args.confidence not in (0,95,99):
    print ("chisq argument invalid; must be either 0,95,99")
    sys.exit()
  print args.confidence
  train_data = []
  # read the file
  read_file(train_data, args.train)

  decision_tree = id3.build_tree(train_data, args.confidence)
  draw_tree(decision_tree, str(args.confidence))
  classify.classify(decision_tree,
                    train_data,
                    True,
                    str(args.confidence),
                    args.ipython)

  validation_data = []
  read_file(validation_data, args.validation)
  classify.classify(decision_tree,
                    validation_data,
                    False, str(args.confidence),
                    args.ipython)

  print 'goodbye'


if __name__ == "__main__":
  """Main entry point, only parses args and passes them on
  """
  parser = argparse.ArgumentParser(
    description =
    "Implements the classic ID3 algorithm for classifying a set of dna promoters.")

  parser.add_argument(
      "-t",
      "--train",
      help = 'the data on which you wish to train e.g. \"../data/training.txt\" ',
      required=True
      )
  parser.add_argument(
      '-v',
      '--validation',
      help = 'the validation data',
      required=True)
  parser.add_argument(
      '--ipython',
      help='this is an ipython session and we want to draw the figs, not save them',
      action='store_true')
  parser.add_argument(
      '-mce',
      help='use the misclassifcation error algorithm',
      action='store_true')
  parser.add_argument(
      '-x',
      '--confidence',
      help='threshold confidence level for growing the decision tree. Can either be (0, 95, 99)',
      type=int
      )
  main(parser)
