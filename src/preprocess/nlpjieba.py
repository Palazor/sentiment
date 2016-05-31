# -*- coding: utf-8 -*-

import jieba
import jieba.posseg

def segment(sentence):
    seg = jieba.posseg.cut(sentence)
    for i in seg:
        print i

    return seg