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

class Classifier:
    classifier = None

    def __init__(self, type='SVC'):
        self.classifier = SklearnClassifier({
            'SVC': SVC(),
            'LogisticRegression': LogisticRegression(),
            'BernoulliNB': BernoulliNB()
        }[type])
        if not self.classifier:
            self.classifier = SklearnClassifier(SVC())

    def train(self, trainset):
        self.classifier.train(trainset)

    def test(self, tagged, featuresets):
        predict = self.classifier.classify_many(featuresets)
        print predict
        return accuracy_score(tagged, predict)

    def classify(self, featureset):
        return self.classifier.classify(featureset)

    def classify_batch(self, featuresets):
        return self.classifier.classify_many(featuresets)

# shuffle(posFeatures)
# shuffle(negFeatures)
#
# # 75% of features used as training set (in fact, it have a better way by using cross validation function)
# size_pos = int(len(pos_review) * 0.75)
# size_neg = int(len(neg_review) * 0.75)
#
# train_set = posFeatures[:size_pos] + negFeatures[:size_neg]
# test_set = posFeatures[size_pos:] + negFeatures[size_neg:]
#
# test, tag_test = zip(*test_set)
#
#
# def clf_score(classifier):
#     classifier = SklearnClassifier(classifier)
#     classifier.train(train_set)
#
#     predict = classifier.batch_classify(test)
#     return accuracy_score(tag_test, predict)
#
#
# print 'BernoulliNB`s accuracy is %f' % clf_score(BernoulliNB())
# print 'GaussianNB`s accuracy is %f' % clf_score(GaussianNB())
# print 'MultinomiaNB`s accuracy is %f' % clf_score(MultinomialNB())
# print 'LogisticRegression`s accuracy is %f' % clf_score(LogisticRegression())
# print 'SVC`s accuracy is %f' % clf_score(SVC(gamma=0.001, C=100., kernel='linear'))
# print 'LinearSVC`s accuracy is %f' % clf_score(LinearSVC())
# print 'NuSVC`s accuracy is %f' % clf_score(NuSVC())
#
#
# # 5. After finding the best classifier, then check different dimension classification accuracy
# def score(classifier):
#     classifier = SklearnClassifier(classifier)
#     classifier.train(trainset)
#
#     pred = classifier.batch_classify(test)
#     return accuracy_score(tag_test, pred)
#
#
# dimention = ['500', '1000', '1500', '2000', '2500', '3000']
#
# for d in dimention:
#     word_scores = create_word_bigram_scores()
#     best_words = find_best_words(word_scores, int(d))
#
#     posFeatures = pos_features(best_word_features_com)
#     negFeatures = neg_features(best_word_features_com)
#
#     # Make the feature set ramdon
#     shuffle(posFeatures)
#     shuffle(negFeatures)
#
#     # 75% of features used as training set (in fact, it have a better way by using cross validation function)
#     size_pos = int(len(pos_review) * 0.75)
#     size_neg = int(len(neg_review) * 0.75)
#
#     trainset = posFeatures[:size_pos] + negFeatures[:size_neg]
#     testset = posFeatures[size_pos:] + negFeatures[size_neg:]
#
#     test, tag_test = zip(*testset)
#
#     print 'BernoulliNB`s accuracy is %f' % score(BernoulliNB())
#     print 'MultinomiaNB`s accuracy is %f' % score(MultinomialNB())
#     print 'LogisticRegression`s accuracy is %f' % score(LogisticRegression())
#     print 'SVC`s accuracy is %f' % score(SVC())
#     print 'LinearSVC`s accuracy is %f' % score(LinearSVC())
#     print 'NuSVC`s accuracy is %f' % score(NuSVC())
#     print
#
#
# # 6. Store the best classifier under best dimension
# def store_classifier(clf, trainset, filepath):
#     classifier = SklearnClassifier(clf)
#     classifier.train(trainset)
#     # use pickle to store classifier
#     pickle.dump(classifier, open(filepath, 'w'))
