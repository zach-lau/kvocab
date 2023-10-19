"""
Main entry point for the vocab scripts
"""

import csv

from konlpy.tag import Hannanum
from collections import defaultdict

from extract import extract_xml
from filter import *

if __name__ == "__main__":
    hannanum = Hannanum(max_heap_size=4096)
    filename = "./data/rhghr10.xml"
    word_dict = defaultdict(lambda : 0)
    for phrase in extract_xml(filename):
        phrase = filter_line(phrase)
        morphs = hannanum.morphs(phrase)
        morphs = filter_morphs(morphs)
        for m in morphs:
            word_dict[m] += 1

    outfile = "out.csv"
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for pair in sorted(word_dict.items(),key = lambda x : x[1], reverse=True):
            writer.writerow(pair)
