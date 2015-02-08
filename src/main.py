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
  # print (tree.adjacency_list())
  # print tree.nodes()
  # print nx.info(tree)
  # print nx.adjacency_matrix(tree)
  graph = nx.to_agraph(tree)
  # print graph
  print graph.layout()
  graph.draw('tree.png')

  # make new labels for edges:
  from pprint import pprint

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
  print [str(node) for node in order]

  # # build tree
  # start = order[0]
  # nodes = [order[0]] # start with first node in topological order
  # labels = {}
  # print "edges"
  # topo_tree = nx.Graph()
  # while nodes:
  #     source = nodes.pop()
  #     labels[source] = source
  #     for target in tree.neighbors(source):
  #         if target in topo_tree:
  #             t = uuid.uuid1() # new unique id
  #         else:
  #             t = target
  #         labels[t] = target
  #         topo_tree.add_edge(source,t)
  #         print source,target,source,t
  #         nodes.append(target)

  # nx.draw(topo_tree,labels=labels)
  # plt.show()

def main(args):
  data = []
  # read the file 
  read_file(data, args.filename)
  tree = id3.build_tree(data)
  draw_tree(tree)
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




