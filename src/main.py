# -*- coding: utf-8 -*-

from preprocess.Preprocess import Preprocess
from feature.Extractor import Extractor
from classifier.Classifier import ClassifierComplex
from dict_score.DictScore import DictScore
import os
import os.path
from random import shuffle

if __name__ == '__main__':
    preprocessor = Preprocess()
    # preprocessor.process_train_samples('../train/')

    extractor = Extractor()
    [train_set, test_set, tag_set] = extractor.prepare_train_set()

    classifier = ClassifierComplex()
    classifier.train(train_set)
    acc = classifier.test(tag_set, test_set)
    print 'accuracy: ', acc


    for parent, dirnames, filenames in os.walk('../train/'):
        for filename in filenames:
            # score = dictScore.score_review(preprocessor.process_segment_by_sentences('../train/' + filename))
            segments = preprocessor.segment('../train/' + filename)
            feature = extractor.extract_one_feature(segments)
            score = classifier.classify(feature)
            print filename, score