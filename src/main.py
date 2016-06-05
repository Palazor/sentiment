# -*- coding: utf-8 -*-

from preprocess.preprocess import process_train_samples
from preprocess.preprocess import process_sample
from feature.Extractor import Extractor
from classifier.Classifier import Classifier
import os
import os.path

if __name__ == '__main__':
    process_train_samples('../train/')

    extractor = Extractor()
    pos = extractor.pos_features
    neg = extractor.neg_features

    size_pos = int(len(pos) * 0.75)
    size_neg = int(len(neg) * 0.75)
    train_set = pos[:size_pos] + neg[:size_neg]
    test_set = pos[size_pos:] + neg[size_neg:]
    test, tag_test = zip(*test_set)

    classifier = Classifier()
    classifier.train(train_set)
    acc = classifier.test(tag_test, test)
    print 'accuracy: ', acc

    # texts = []
    # for parent, dirnames, filenames in os.walk('../train/'):
    #     for filename in filenames:
    #         texts.append(process_sample('../train/' + filename))
    # feature = extractor.extract_feature(texts)
    # print classifier.classify_batch(feature)

    # feature = extractor.extract_feature([u"导航很灵敏"])
    # print classifier.classify(feature[0])
    print classifier.classify_batch(test)