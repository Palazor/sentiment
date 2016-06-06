# -*- coding: utf-8 -*-

from preprocess.preprocess import process_train_samples
from preprocess.preprocess import process_sample
from feature.Extractor import Extractor
from classifier.Classifier import Classifier
from dict_score.DictScore import DictScore
import os
import os.path

if __name__ == '__main__':
    # process_train_samples('../train/')

    # extractor = Extractor()
    # pos = extractor.pos_features
    # neg = extractor.neg_features
    #
    # size_pos = int(len(pos) * 0.75)
    # size_neg = int(len(neg) * 0.75)
    # train_set = pos[:size_pos] + neg[:size_neg]
    # test_set = pos[size_pos:] + neg[size_neg:]
    # test, tag_test = zip(*test_set)
    #
    # classifier = Classifier('BernoulliNB')
    # classifier.train(train_set)
    # acc = classifier.test(tag_test, test)
    # print 'accuracy: ', acc
    #
    # texts = []
    # for parent, dirnames, filenames in os.walk('../train/'):
    #     for filename in filenames:
    #         texts.append(process_sample('../train/' + filename))
    # feature = extractor.extract_feature(texts)
    # print classifier.classify_batch(feature)

    dictScore = DictScore()
    dictScore.score_review(process_sample('../train/1.docx'))