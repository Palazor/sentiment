# -*- coding: utf-8 -*-

import nltk
import xlrd
import time

grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def get_terms(tree):
    for leaf in leaves(tree):
        term = [ w for w, t in leaf ]
        yield term

def _parsePhrase(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    chunker = nltk.RegexpParser(grammar)
    tree = chunker.parse(tagged)

    terms = get_terms(tree)

    # # print sentence
    # for term in terms:
    #     for word in term:
    #         print word
    # print "###############################################"


def parsePhrase(tagged):
    _grammar = ''
    chunker = nltk.RegexpParser(_grammar)
    tree = chunker.parse(tagged)

    terms = get_terms(tree)


start = time.time()
# data = xlrd.open_workbook('20160414075529005.xls')
# table = data.sheets()[0]
# titles = table.col_values(1)
# for uTitle in titles:
#     title = uTitle.encode('utf-8')
#     parsePhrase(title)
_parsePhrase('Python is a widely used high-level, general-purpose, interpreted, dynamic programming language.')
print time.time() - start