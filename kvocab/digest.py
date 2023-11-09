#!/usr/bin/env python3
"""
Main entry point for the vocab scripts
"""

import os.path

from kvocab.extract import *
from kvocab.filter import *
from kvocab.helpers import *

from kvocab.korean_morph import k_morph
from kvocab.canto_morph import canto_morph

def digest(filename, language):
    if language == 1:
        morph_tagger = k_morph()
    elif language == 2:
        morph_tagger = canto_morph()
    else:
        print("Invalid langauge")
        return
    word_dict = {}
    for phrase in extract(filename):
        pos = morph_tagger.get_morphs(phrase)    
        for p in pos:
            if not p in word_dict:
                word_dict[p] = [1, phrase.replace('\n', ' ')] # count, example
            else:
                word_dict[p][0] += 1
    outfile = os.path.splitext(filename)[0] + ".csv"
    print(f"Writing out to {outfile}")
    write_out(outfile, word_dict)
    return outfile
