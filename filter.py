"""
filter.py

Contains filtering functions for morphemes and lines
"""
# -*- coding: utf-8 -*-

import re

def filter_line(line):
    """
    Filter undesired patterns from a line, such as between brackets or music notes
    """
    p = re.compile(r'\(.*?\) | \[.*?\]', re.VERBOSE)
    return p.sub('', line)

def filter_morphs(morphs):
    """
    Filter out illegal morphs
    """
    # chinese_punctuation = "！，？" # These are slightly different from their romain counterparts
    punctuation = "?,!.'\":-" 
    banned_words = ["...", "♪", "！", "，", "？", "〝", "〞", "、"]
    def strip(m):
        """ Remove punctuation and whitespace"""
        # Remove punctuation or digits
        m = re.sub(f'[{punctuation}]|\\d', '', m)
        return m.strip()
    morphs = map(strip, morphs)
    def valid(m):
        if m in banned_words:
            return False
        if len(m) == 0:
            return False
        return True
    # print(list(morphs))
    morphs = filter(valid, morphs)
    # print(list(morphs))
    return list(morphs)
    
def filter_pos(pos_list):
    def valid(pos):
        valid_pos = ["Noun", "Verb", "Adjective", "Exclamation"]
        if pos[1] not in valid_pos:
            return False
        return True
    sol = filter(valid, pos_list)
    return sol

if __name__ == '__main__':
    print(filter_morphs([u'？']))
