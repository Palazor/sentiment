# -*- coding: utf-8 -*-

import jieba
import jieba.posseg

def segment(sentence):
    seg = jieba.cut(sentence)
    # seg = jieba.posseg.cut(sentence)

    return seg