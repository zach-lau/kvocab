from morph_analyzer import morph_analyzer
from konlpy.tag import Okt
from filter import *

class k_morph(morph_analyzer):
    def __init__(self):
        self.okt = Okt()
    def get_morphs(self, phrase):
        phrase = filter_line(phrase)
        pos = self.okt.pos(phrase, norm=True, stem=True)
        pos = filter_pos(pos)
        return pos
