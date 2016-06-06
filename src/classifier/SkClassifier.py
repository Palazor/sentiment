# -*- coding: utf-8 -*-

from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import accuracy_score


class SKClassifier:

    classifier = None

    def __init__(self, cls='SVC'):
        self.classifier = SklearnClassifier({
            'SVC': SVC(),
            'LogisticRegression': LogisticRegression(),
            'BernoulliNB': BernoulliNB()
        }[cls])
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

    def classify_many(self, featuresets):
        return self.classifier.classify_many(featuresets)

#     pickle.dump(classifier, open(filepath, 'w'))
