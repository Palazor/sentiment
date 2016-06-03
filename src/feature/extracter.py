# -*- coding: utf-8 -*-
import pickle
import itertools
from random import shuffle

import json
import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

import sklearn
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import accuracy_score

def _get_bigram_scores(posdata, negdata):
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

def _find_best_words(word_scores, number):
    best_vals = sorted(word_scores.iteritems(), key=lambda (word, score): score, reverse=True)[:number]
    best_words = set([word for word, score in best_vals])
    return best_words

def _filter_words(words, best_words):
    d1 = dict([(word, True) for word in words if word in best_words])
    d2 = dict([(word, True) for word in nltk.bigrams(words) if word in best_words])
    d3 = dict(d1, **d2)
    return d3

def extract_feature():
    f = open('../test/pos_review.txt')
    pos_data = json.loads(f.readline(), 'utf-8')
    f.close()
    f = open('../test/neg_review.txt')
    neg_data = json.loads(f.readline(), 'utf-8')
    f.close()

    word_scores = _get_bigram_scores(pos_data, neg_data)
    best_words = _find_best_words(word_scores, 1500)

    pos_features = []
    for review in pos_data:
        feature = [_filter_words(review, best_words), 'pos']
        pos_features.append(feature)

    neg_features = []
    for review in neg_data:
        feature = [_filter_words(review, best_words), 'neg']
        neg_features.append(feature)

    return [pos_features, neg_features]
