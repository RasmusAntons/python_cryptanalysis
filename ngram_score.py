"""
Allows scoring of text using n-gram probabilities
17/07/12
"""
from math import log10


class NgramScore(object):
    __cache = {}

    def __init__(self, ngramfile, sep=' '):
        """ load a file containing ngrams and counts, calculate log probabilities """
        self.ngramfile = ngramfile
        self.sep = sep
        self.ngrams = None

    def load(self):
        if self.ngramfile in NgramScore.__cache:
            self.ngrams = NgramScore.__cache[self.ngramfile]
        else:
            self.ngrams = {}
            for line in open(self.ngramfile):
                key, count = line.split(self.sep)
                self.ngrams[key] = int(count)
            self.L = len(key)
            self.N = sum(self.ngrams.values())
            # calculate log probabilities
            for key in self.ngrams.keys():
                self.ngrams[key] = log10(self.ngrams[key] / self.N)
            self.floor = log10(0.01 / self.N)
            NgramScore.__cache[self.ngramfile] = self.ngrams

    def score(self, text):
        """ compute the score of text """
        if self.ngrams is None:
            self.load()
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor
        return score
