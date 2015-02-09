# Decision Tree Project

Builds a decision tree classifier for the UCI promoter dataset.

# REQUIREMENTS:
There are several dependencies:
* [NetworkX](https://networkx.github.io/)
* [Numpy](http://www.numpy.org/)
* [pygraphviz](http://pygraphviz.github.io/)
* [matplotlib](http://matplotlib.org/)
* [graphviz](http://www.graphviz.org/)

I believe all of them may be installed with PIP or easy_install:
```
pip install networkx
```
or
```
easy_install -U networkx
```
# Running
The program may be ran like this:
```
$ python main.py -h
usage: main.py [-h] -t TRAIN -v VALIDATION [--ipython] [-mce] [-x CONFIDENCE]

Implements the classic ID3 algorithm for classifying a set of dna promoters.

optional arguments:
  -h, --help            show this help message and exit
  -t TRAIN, --train TRAIN
                        the data on which you wish to train e.g.
                        "../data/training.txt"
  -v VALIDATION, --validation VALIDATION
                        the validation data
  --ipython             this is an ipython session and we want to draw the
                        figs, not save them
  -mce                  use the misclassifcation error algorithm
  -x CONFIDENCE, --confidence CONFIDENCE
                        threshold confidence level for growing the decision
                        tree. Can either be (0, 95, 99)
```
 
Example, for specifying a 95% confidence level
```
python main.py --train ../data/training.txt --validation
 ../data/validation.txt --confidence 95
```
and the program will write several plots to your current directory.
