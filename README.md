# Decision Tree Project
Aaron Gonzales

agonzales@cs.unm.edu

2015-02-08

Builds a decision tree classifier for the UCI promoter dataset.
Report can be found
[here](http://nbviewer.ipython.org/github/xysmas/decision_trees/blob/master/src/decision_tree_report.ipynb)

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

# Installing
You may download the repositiory from this link https://github.com/xysmas/decision_trees/archive/master.zip
or just unzip the attached file:

  unzip agonzales_decision_tree.zip

In the created directory, there will be this README.md file (can be opened with
any real text editor), a data directory, and a src directory
navigate to the src directory and you may run it from there

# Running
The program may be ran like this:

```
usage: main.py [-h] -t TRAIN -v VALIDATION [--ipython] -x CONFIDENCE

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
  -x CONFIDENCE, --confidence CONFIDENCE
                        threshold confidence level for growing the decision
                        tree. Can either be (0, 95, 99)
```

For example, running and specifying a 95% confidence level:
```
python main.py --train ../data/training.txt --validation ../data/validation.txt --confidence 95
```
and the program will write several plots to your current directory while
displaying minor output.
