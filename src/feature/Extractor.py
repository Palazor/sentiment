# -*- coding: utf-8 -*-
import pickle
import itertools
from random import shuffle

import json
import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

class Extractor():
    pos_data = []
    neg_data = []
    best_words = None
    pos_features = None
    neg_features = None

    def __init__(self):
        if not self.best_words:
            # f = open('../test/pos_review.txt')
            # self.pos_data = json.loads(f.readline(), 'utf-8')
            # f.close()
            f = open('../test/pos_features.txt')
            self.pos_data += json.loads(f.readline(), 'utf-8')
            f.close()
            # f = open('../test/neg_review.txt')
            # self.neg_data = json.loads(f.readline(), 'utf-8')
            # f.close()
            f = open('../test/neg_features.txt')
            self.neg_data += json.loads(f.readline(), 'utf-8')
            f.close()

            word_scores = self._get_bigram_scores(self.pos_data, self.neg_data)
            self.best_words = self._find_best_words(word_scores)

            self.pos_features = []
            for review in self.pos_data:
                feature = [self._filter_words(review, self.best_words), 'pos']
                self.pos_features.append(feature)
            shuffle(self.pos_features)

            self.neg_features = []
            for review in self.neg_data:
                feature = [self._filter_words(review, self.best_words), 'neg']
                self.neg_features.append(feature)
            shuffle(self.neg_features)

    def _get_bigram_scores(self, posdata, negdata):
        pos_words = list(itertools.chain(*posdata))
        neg_words = list(itertools.chain(*negdata))

        pos_bigram_finder = BigramCollocationFinder.from_words(pos_words)
        neg_bigram_finder = BigramCollocationFinder.from_words(neg_words)
        pos_bigrams = pos_bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)
        neg_bigrams = neg_bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)

        pos = pos_words + pos_bigrams
        neg = neg_words + neg_bigrams

        word_fd = FreqDist()
        cond_word_fd = ConditionalFreqDist()
        for word in pos:
            word_fd[word] += 1
            cond_word_fd['pos'][word] += 1
        for word in neg:
            word_fd[word] += 1
            cond_word_fd['neg'][word] += 1

        pos_word_count = cond_word_fd['pos'].N()
        neg_word_count = cond_word_fd['neg'].N()
        total_word_count = pos_word_count + neg_word_count

        word_scores = {}
        for word, freq in word_fd.iteritems():
            pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
            neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
            word_scores[word] = pos_score + neg_score

        return word_scores

    def _find_best_words(self, word_scores, number = None):
        best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)
        if number and number > 0:
            best_vals = best_vals[:number]
        best_words = set([w for w, s in best_vals])
        return best_words

    def _filter_words(self, words, best_words):
        d1 = dict([(word, True) for word in words if word in best_words])
        # return d1
        d2 = dict([(word, True) for word in nltk.bigrams(words) if word in best_words])
        d3 = dict(d1, **d2)
        return d3

    def extract_feature(self, review_data, polar=None):
        features = []
        for review in review_data:
            if polar:
                feature = [self._filter_words(review, self.best_words), polar]
            else:
                feature = self._filter_words(review, self.best_words)
            features.append(feature)
        return features
