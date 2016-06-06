# -*- coding: utf-8 -*-

from sklearn.metrics import accuracy_score

from DictScoreClassifer import DictScoreClassifier
from SkClassifier import SKClassifier

class ClassifierComplex:

    dict_clf = None
    svc_clf = None
    nb_clf = None

    def __init__(self):
        self.dict_clf = DictScoreClassifier()
        self.svc_clf = SKClassifier('SVC')
        self.nb_clf = SKClassifier('BernoulliNB')

    def train(self, trainset):
        self.dict_clf.train(trainset[1])
        self.svc_clf.train(trainset[0])
        self.nb_clf.train(trainset[0])

    def test(self, tagged, featuresets):
        predict = self.classify_many(featuresets)
        return accuracy_score(tagged, predict)

    def classify(self, featureset):
        score = 0
        predict_dict = self.dict_clf.classify(featureset[1])
        score += 0.65 if predict_dict == 'pos' else -0.65
        predict_svc = self.svc_clf.classify(featureset[0])
        score += 0.15 if predict_svc == 'pos' else -0.15
        predict_nb = self.nb_clf.classify(featureset[0])
        score += 0.2 if predict_nb == 'pos' else -0.2

        return 'pos' if score > 0 else 'neg'

    def classify_many(self, featuresets):
        return [self.classify(feature) for feature in zip(featuresets[0],featuresets[1])]

#     pickle.dump(classifier, open(filepath, 'w'))
