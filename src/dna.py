"""class for DNA object."""
__author__ = "Aaron Gonzales"
__copyright__ = "GPL"
__license__ = "GPL"
__maintainer__ = "Aaron Gonzales"
__email__ = "agonzales@cs.unm.edu"
__status__ = "Development"

class DNA(object):
    """ Main class for DNA objects.
    Holds relevent information about the dna, including promoter type, name, and
    sequence.

    Args:
        promoter (Boolean): One of {+/-}, indicating the class ("+" = promoter).
        sequence (list): The remaining 57 fields are the sequence, starting at
                 position -50 (p-50) and ending at position +7 (p7). Each of
                 these fields is filled by one of {a, g, t, c}.
    Attributes:
        features: Dictionary of the above sequence.
        """
    def __init__(self, sequence, promoter):
        self.sequence = list(sequence)
        if promoter is '+':
            self.promoter = True
        else:
            self.promoter = False

        # make a dict with key of feature number and val of the base
        index = range(0, len(sequence))
        self.features = {}
        for index, feature in zip(index, sequence):
            self.features[index] = feature

    def __str__(self):
        return ('DNA object: \n ' +
                '\n promoter: ' + str(self.promoter))

    def get_info(self):
        """Returns a debugging statement about the object"""
        print(" -- Debug: DNA object promoter class: %s " % self.promoter)
        print(" -- Debug: DNA object sequence class: %s " % self.sequence)
        print(" -- Debug: DNA object features class: %s " % self.features)

    def base_at_index(self, index):
        """Returns the base of this dna at a given index. for convenience"""
        return self.sequence[index]

