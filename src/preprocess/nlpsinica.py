# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import sinica_treebank

sinica_text = nltk.Text(sinica_treebank.words())
print sinica_text
for (key, var) in sinica_treebank.tagged_words()[:8]:
    print '%s/%s' % (key, var)

print sinica_treebank.parsed_sents()[15]