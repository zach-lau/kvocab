"""
Main entry point for the vocab scripts
"""

import csv

# from konlpy.tag import Hannanum
from konlpy.tag import Okt
from collections import defaultdict

from extract import *
from filter import *

if __name__ == "__main__":
    # hannanum = Hannanum(max_heap_size=4096)
    okt = Okt()
    # filename = "./data/rhghr10.xml"
    filename = "./data/mlfts8.vtt"
    word_dict = defaultdict(lambda : 0)
    for phrase in extract(filename):
        phrase = filter_line(phrase)
        # morphs = hannanum.morphs(phrase)
        # morphs = filter_morphs(morphs)
        pos = okt.pos(phrase, norm=True, stem=True)
        pos = filter_pos(pos)
        for p in pos:
            word_dict[p] += 1

    outfile = "out.csv"
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for pair in sorted(word_dict.items(),key = lambda x : x[1], reverse=True):
            pos_pair, count = pair
            word, pos = pos_pair
            writer.writerow([word, pos, count])
