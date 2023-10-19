"""
filter.py

Contains filtering functions for morphemes and lines
"""
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
    punctuation = "?,!.'\":-"
    banned_words = ["...", "♪"]
    def valid(m):
        if m in punctuation:
            return False
        if m in banned_words:
            return False
        return True
    return filter(valid, morphs)
