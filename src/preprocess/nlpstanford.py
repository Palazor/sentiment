# -*- coding: utf-8 -*-

from nltk.tokenize.stanford_segmenter import StanfordSegmenter

def segment(sentence):
    path = '/media/razor/Files/Python27/nltk_data/stanford-segmenter-2015-12-09/'
    segmenter = StanfordSegmenter(path + 'stanford-segmenter-3.6.0.jar', path + 'slf4j-api.jar', path + 'data/pku.gz', path + 'data/dict-chris6.ser.gz')

    return segmenter.segment(u'我爱北京天安门')