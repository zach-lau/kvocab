import pycantonese
from .filter import *
from .morph_analyzer import morph_analyzer

class canto_morph(morph_analyzer):
    def __init__(self):
        pass
    def get_morphs(self, phrase):
        phrase = filter_line(phrase)
        words = pycantonese.segment(phrase)
        morphs = filter_morphs(words)
        pos = pycantonese.pos_tag(morphs)
        return pos
