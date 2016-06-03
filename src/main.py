# -*- coding: utf-8 -*-

from preprocess.preprocess import process_train_samples
from preprocess.preprocess import process_sample
from feature.extracter import extract_feature

if __name__ == '__main__':
    process_train_samples('../train/')
    extract_feature()

    process_sample('../train/1.docx')