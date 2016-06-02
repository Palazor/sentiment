# -*- coding: utf-8 -*-

from preprocess.preprocess import process_samples
from preprocess.preprocess import extract_feature_unigram

if __name__ == '__main__':
    samples = process_samples('../train/')
    sample_features = extract_feature_unigram(samples)