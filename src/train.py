""" 
main.py is the primary file that runs the decsion tree parser
"""
import id3
from feature import feature
from dna import DNA
from main import read_file


# graph tool
try:
  import networkx as nx
  from networkx import graphviz_layout
  import pygraphviz as pgv
  import matplotlib.pyplot as plt
except ImportError:
  raise ImportError('This program requires Graphviz, pygraphviz, networkx, and matplotlib')


__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"

get_accuracy(d_tree, test_data):
  """ gets the accuracy of a given file based on the built decision tree.
  Args:
    d_tree (networkx tree): the built decision tree
    test_data (list) of 
  Return: (list) the results?
  """


