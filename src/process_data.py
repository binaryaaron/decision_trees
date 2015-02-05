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

__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"
__status__ = "Development"
__version__ = "0.1"
__date__ = "2015-01-20"



"""
  # class here for the DNA object
# that should include the classification (promoter / not), 
# instance name, and sequence as fields in the object
# main will create objects when ran

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DNA Promoter ID3 classifer")
    parser.add_argument("filename", 
        help = 'the DNA promoter data file')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
      reader = csv.reader(f, delimiter=',')
      for line in f:
        print line

    print 'done'
