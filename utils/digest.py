#!/usr/bin/env python3
"""
Main entry point for the vocab scripts
"""

import os.path
import argparse

from kvocab.extract import *
from kvocab.filter import *
from kvocab.helpers import *

from kvocab.korean_morph import k_morph
from kvocab.canto_morph import canto_morph

def digest(filename, language = "ko"):
    if language == "ko":
        morph_tagger = k_morph()
    elif language == "yue":
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'digest',
        description = 'Process subtite file and produce sorted list of morphemes',
    )
    parser.add_argument(
        "language",
        choices = ['ko','yue'],
    )
    parser.add_argument(
        'files',
        nargs=argparse.REMAINDER
    )
    args = parser.parse_args()
    # print(args.language)
    # print(args.files)
    for file in args.files:
        print(f"Parsing {file}")
        digest(file, args.language)
    
    # if len(sys.argv) > 1:
    #     filename = sys.argv[1]
    #     for file in sys.argv[1:]:
    #         try:
    #             digest(file)
    #         except:
    #             print(f"Couldn't parse file {file}")
    # else:
    #     digest("./data/mlfts14.vtt")
    # # digest("./data/id.xml", language="canto") 