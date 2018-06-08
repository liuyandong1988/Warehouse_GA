# -*- encoding: utf-8 -*-
SCORE_NONE = -1
class Life(object):
    """chromosome"""
    def __init__(self, aGene = None):
        self.gene = aGene
        self.score = SCORE_NONE
