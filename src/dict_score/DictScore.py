# -*- coding: utf-8 -*-

import json

class DictScore:
    weight = None
    pos_words = None
    neg_words = None

    def __init__(self):
        f = open('../sentiment/dict-weight.txt')
        self.weight = json.loads(''.join(''.join(f.readlines()).split('\n')), 'utf-8')
        f.close()
        f = open('../sentiment/dict-pos.txt')
        self.pos_words = ''.join(f.readlines()).decode('utf-8').split('\n')
        f.close()
        f = open('../sentiment/dict-neg.txt')
        self.neg_words = ''.join(f.readlines()).decode('utf-8').split('\n')
        f.close()


    def _get_weight(self, word):
        if self.weight.has_key(word):
            return self.weight[word]
        else:
            return 1


    def score_review(self, feature):
        pos_score = 0
        neg_score = 0
        cur_pos = 0
        sen_pos = 0
        for word in feature:
            if word in self.pos_words:
                pos_score += 1
                for preword in feature[sen_pos:cur_pos]:
                    pos_score *= self._get_weight(preword)
                sen_pos += 1
                print word
            elif word in self.neg_words:
                neg_score += 1
                for preword in feature[sen_pos:cur_pos]:
                    neg_score *= self._get_weight(preword)
                sen_pos += 1
                print word
            cur_pos += 1

        print pos_score, neg_score
