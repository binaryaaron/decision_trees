""" 
classify.py searches through the data and gives classifications.
"""
import numpy as np
import matplotlib.pyplot as plt
import id3 as id3
import feature
from Queue import Queue

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"


def search_tree(d_tree, root, dna_n):
  """ traversal of the tree to find classification
  Args:
    d_tree (networkx) d_treeraph: the decision tree
    root (root node):
    dna (DNA): the sequence to classify
  """
  # print "root node is at index: %d " % root.index
  q = Queue()
  q.put(root)
  while q.empty() is False:
    current_node = q.get()
    base = dna_n.base_at_index(current_node.index)
    # print ('current node: id: %d,  leaf: %s, label = %s ' %
    #     (current_node.index, current_node.is_leaf, current_node.label))
    if current_node.is_leaf:
      # print "i'm a leaf and have label of %s " % str(current_node.label)
      return current_node.label
    if current_node.is_leaf is False:
      # print 'following the base %s' % base
      # d_treeet the node at the end of the edd_treee in this node/seq pair
      # make the successor edges of the root to test following
      child_edges = [(current_node, node) for node in d_tree.successors(current_node)]
      for u,v in child_edges:
        e =  d_tree.get_edge_data(u,v)
        # print e
        # print (u.index, v.index)
        # follow the right edge:
        if e['base'] is base:
          q.put(v)
          break


def classify(d_tree, test_data, train):
  """ gets the accuracy of a given file based on the built decision tree.
  Args:
    d_tree (networkx tree): the built decision tree
    test_data (list): data to classify
    train (boolean): flag to specify it this is a train set or validation set
  Return: (list) the results?
  """
  fig_name = ''
  if train:
    fig_name = 'training'
  else:
    fig_name = 'validation'
  DEBUG = True
  if DEBUG:
    from pprint import pprint
  if test_data is None:
    raise TypeError('The test data is empty')
  root = 0
  # can't use list comp with error checking, since networkx has multiple things
  # as node types
  for node in d_tree.nodes():
    try:
      if node.is_root is True:
        root = node
    except AttributeError:
      # print ("found a leaf")
      continue
  # print 'got a root node at index: %d' %root.index
  # # label = search_tree(d_tree, root, test_data)
  # finished_data = [(d.promoter, search_tree(d_tree,root,d)) for d in test_data]
  labels = [ '+' == search_tree(d_tree,root,d) for d in test_data]
  # pprint(labels)
  promoters = [p.promoter for p in test_data]
  # joins the promoter and label lists, putting them as strings and notbooleans
  results = [(str(p), str(l)) for p,l in zip(promoters, labels)]
  # finished = zip(promoters, labels)
  # pprint (finished)
  labels = ['True', 'False']
  matrix = confusion_matrix(results, labels)
  print(matrix)
  plot(matrix, labels)
  plt.title('Confusion matrix for ' + fig_name)
  plt.savefig('confusion_matrix_' +fig_name + '.pdf')


def confusion_matrix(results, labels):
  """Builds a confusion matrix from the result data.
  Args:
    results (list): list of tuples with real and predicted values
    labels (list): labels
  """
  output = np.zeros((len(labels), len(labels)), dtype=float)
  for predicted, real in results:
      output[labels.index(predicted), labels.index(real)] += 1
  return output / output.sum(axis=1)[:, None]

def plot(matrix, labels):
  """ Plots the matrix using Numpy/Matplotlib
  Args:
    matrix (np matrix): the confusion matrix
    labels (list): the labels for promoters
  """
  fig, ax = plt.subplots()
  im = ax.matshow(matrix)
  cb = fig.colorbar(im)
  cb.set_label('Percentage Correct')

  ticks = range(len(labels))
  ax.set(xlabel='True Label',
         ylabel='Predicted Label',
         xticks=ticks,
         xticklabels=labels,
         yticks=ticks,
         yticklabels=labels)
  ax.xaxis.set(label_position='bottom')
  return fig
