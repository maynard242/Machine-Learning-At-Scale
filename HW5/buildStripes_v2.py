#!~/opt/anaconda2/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import re
import mrjob
import json
from mrjob.protocol import RawProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep
import itertools

class MRbuildStripes(MRJob):
    SORT_VALUES = True
    
    def mapper(self, _, line):
        fields = line.lower().strip("\n").split("\t")
        words = fields[0].split(" ")
        occurrence_count = int(fields[1])
        for subset in itertools.combinations(sorted(set(words)), 2):
            yield subset[0], (subset[1], occurrence_count)
            yield subset[1], (subset[0], occurrence_count)
    
    def reducer(self, word, occurrence_counts):
        stripe = {}
        for other_word, occurrence_count in occurrence_counts:
            stripe[other_word] = stripe.get(other_word,0)+occurrence_count
        yield word, stripe

if __name__ == '__main__':
    MRbuildStripes.run()