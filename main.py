"""
Main entry point for the vocab scripts
"""

import csv
import os.path
# from konlpy.tag import Hannanum
from konlpy.tag import Okt
from collections import defaultdict

from extract import *
from filter import *

def digest(filename):
    # hannanum = Hannanum(max_heap_size=4096)
    okt = Okt()
    word_dict = defaultdict(lambda : 0)
    for phrase in extract(filename):
        phrase = filter_line(phrase)
        # morphs = hannanum.morphs(phrase)
        # morphs = filter_morphs(morphs)
        pos = okt.pos(phrase, norm=True, stem=True)
        pos = filter_pos(pos)
        for p in pos:
            word_dict[p] += 1

    outfile = os.path.splitext(filename)[0] + ".csv"
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for pair in sorted(word_dict.items(),key = lambda x : x[1], reverse=True):
            pos_pair, count = pair
            word, pos = pos_pair
            writer.writerow([word, pos, count])

if __name__ == "__main__":
    digest("./data/mlfts14.vtt")
    