"""
Main entry point for the vocab scripts
"""

import os.path
from collections import defaultdict

from extract import *
from filter import *
from helpers import *

from korean_morph import k_morph
from canto_morph import canto_morph

def digest(filename, language = "ko"):
    if language == "ko":
        morph_tagger = k_morph()
    elif language == "canto":
        morph_tagger = canto_morph()
    else:
        print("Invalid langauge")
        return
    word_dict = {}
    for phrase in extract(filename):
        pos = morph_tagger.get_morphs(phrase)    
        for p in pos:
            if not p in word_dict:
                word_dict[p] = [1, phrase] # count, example
            else:
                word_dict[p][0] += 1
    outfile = os.path.splitext(filename)[0] + ".csv"
    print(f"Writing out to {outfile}")
    write_out(outfile, word_dict)

if __name__ == "__main__":
    digest("./data/mlfts14.vtt")
    # digest("./data/id.xml", language="canto") 