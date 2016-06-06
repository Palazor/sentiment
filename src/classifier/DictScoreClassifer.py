# -*- coding: utf-8 -*-

from dict_score.DictScore import DictScore


class DictScoreClassifier:

    dict_score = None
    threshold = 0

    def __init__(self):
        self.dict_score = DictScore()

    def train(self, trainset):
        tagged = []
        predict = []
        for sample in trainset:
            score = self.dict_score.score_review(sample[0])
            predict.append(score)
            tagged.append(sample[1])

        self.threshold = -1
        max_hit = 0
        for threshold in range(-1000, 1000):
            hit = len([1 for (score, tag) in zip(predict, tagged) if (score > threshold and tag == 'pos') or (score <= threshold and tag=='neg')])
            if hit > max_hit:
                max_hit = hit
                self.threshold = float(threshold) / 1000
        print self.threshold

    def classify(self, featureset):
        return 'pos' if self.dict_score.score_review(featureset) > self.threshold else 'neg'

    def classify_many(self, featuresets):
        return [self.classify(feature) for feature in featuresets]