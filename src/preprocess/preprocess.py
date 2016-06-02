# -*- coding: utf-8 -*-

import os
import os.path
import zipfile
from lxml import etree
import json
import nltk
nltk.data.path.append('/media/razor/Files/Python27/nltk_data')
from nlpjieba import segment
from phrase import parsePhrase

punt_list = u',.!?:;~，。！？：；～'

def getXml(docxFilename):
    zip = zipfile.ZipFile(open(docxFilename))
    xmlContent = zip.read("word/document.xml")
    zip.close()
    return xmlContent


def getXmlTree(xmlContent):
    return etree.fromstring(xmlContent)


def docx2txt(docx_string):
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'

    tree = getXmlTree(docx_string)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            para = ''.join(texts)
            paragraphs.append(para)
            # tokens = nltk.word_tokenize(para)
            # tagged = nltk.pos_tag(tokens)
    result = '\n\n'.join(paragraphs)

    return result


def parseSentence(sentence):
    print '==================================='
    print sentence
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    print tagged


def refineSentence(text):
    parts = [text]
    delimiters = ['.', '!', '?', ';', ':', u'。', u'！', u'？', u'；', u'：']
    for deli in delimiters:
        sub = []
        for item in parts:
            sub.extend(item.split(deli))
        parts = sub

    return parts


def cut_sentence(words):
    start = 0
    i = 0
    sents = []
    for word in words:
        if word in punt_list:
            sents.append(words[start:i+1])
            start = i + 1  #start标记到下一句的开头
            i += 1
        else:
            i += 1  #若不是标点符号，则字符位置继续前移
    if start < len(words):
        sents.append(words[start:])  #这是为了处理文本末尾没有标点符号的情况
    return sents


def parseDocx(docx_string):
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    R = WORD_NAMESPACE + 'r'
    COLOR = WORD_NAMESPACE + 'color'
    TEXT = WORD_NAMESPACE + 't'
    VALUE = WORD_NAMESPACE + 'val'

    POS = 'FF0000'
    NEG = '00B050'

    tree = getXmlTree(docx_string)
    sentences = []
    sentence = ''
    pos = []
    neg = []
    for seg in tree.getiterator(R):
        text = None
        for nodeText in seg.iter(TEXT):
            text = nodeText.text
        if not text:
            continue
        text = text.replace(' ', '').replace('\t', '').replace(u'　', '')
        if text == '':
            continue

        color = None
        for nodeColor in seg.getiterator(COLOR):
            color = nodeColor.attrib[VALUE]
        if color == POS:
            pos.append((len(sentence), text))
        elif color == NEG:
            neg.append((len(sentence), text))

        frags = cut_sentence(text)
        sentence += frags[0]
        numS = len(frags)
        if numS > 1:
            sentences.append([sentence, pos, neg])
            pos = []
            neg = []
            sentence = ''
            for i in range(1, numS - 1):
                sentences.append([frags[i], [], []])
                pos = []
                neg = []
            if numS >= 2:
                sentence = frags[numS - 1]
    sentences.append([sentence, pos, neg])

    return sentences


def process_samples(path):
    # poses = {}
    # pos_count = {}
    s_array = []
    p_array = []
    n_array = []
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # print filename
            sentences = parseDocx(getXml(path + filename))

            # f = open('../test/sentences.txt', 'w+')
            # f.write(json.dumps(sentences, ensure_ascii=False).encode('utf-8'))
            # f.close()

            for sentence in sentences:
                s = sentence[0]
                pos = sentence[1]
                neg = sentence[2]
                segs = segment(s)

                length = 0
                p = 0
                n = 0
                p_pos = None
                p_term = None
                if len(pos) > 0 and p < len(pos):
                    p_pos = pos[p][0]
                    p_term = pos[p][1]
                n_pos = None
                n_term = None
                if len(neg) > 0 and n < len(neg):
                    n_pos = neg[n][0]
                    n_term = neg[n][1]
                for term in segs:
                    num = len(term)
                    if p_pos and length == p_pos:
                        p_len = len(p_term)
                        p_array.append(len(s_array))
                        length += num
                        if num < p_len:
                            s_array.append(term)
                            p_pos = length
                            p_term = p_term[num: 100]
                        else:
                            s_array.append(p_term)
                            p += 1
                            if p < len(pos):
                                p_pos = pos[p][0]
                                p_term = pos[p][1]
                            else:
                                p_pos = None
                                p_term = None
                            if num > p_len:
                                s_array.append(term[p_len: num])
                    elif p_pos and length + num > p_pos:
                        s_array.append(term[0: p_pos - length])
                        p_array.append(len(s_array))
                        s_array.append(p_term)
                        left = term[p_pos - length + len(p_term): num]
                        if left != '':
                            s_array.append(left)
                        length += num
                        p += 1
                        if p < len(pos):
                            p_pos = pos[p][0]
                            p_term = pos[p][1]
                        else:
                            p_pos = None
                            p_term = None
                    elif n_pos and length == n_pos:
                        n_len = len(n_term)
                        n_array.append(len(s_array))
                        length += num
                        if num < n_len:
                            s_array.append(term)
                            n_pos = length
                            n_term = n_term[num: 100]
                        else:
                            s_array.append(n_term)
                            n += 1
                            if n < len(neg):
                                n_pos = neg[n][0]
                                n_term = neg[n][1]
                            else:
                                n_pos = None
                                n_term = None
                            if num > n_len:
                                s_array.append(term[n_len: num])
                    elif n_pos and length + num > n_pos:
                        s_array.append(term[0: n_pos - length])
                        n_array.append(len(s_array))
                        s_array.append(n_term)
                        left = term[n_pos - length + len(n_term): num]
                        if left != '':
                            s_array.append(left)
                        length += num
                        n += 1
                        if n < len(neg):
                            n_pos = neg[n][0]
                            n_term = neg[n][1]
                        else:
                            n_pos = None
                            n_term = None
                    else:
                        s_array.append(term)
                        length += num

    # for index in range(0, len(s_array)):
    #     term = s_array[index]
    #     if index in p_array:
    #         print '+' + term + '+'
    #     elif index in n_array:
    #         print '-' + term + '-'
    #     else:
    #         print term

    coarse_sample = [s_array, p_array, n_array]
    # f = open('../test/coarse_sample.txt', 'w+')
    # f.write(json.dumps(coarse_sample, ensure_ascii=False).encode('utf-8'))
    # f.close()

    return coarse_sample

                # index = 0
                # length = 0
                # for item in p:
                #     term = item[1]
                #     while length < item[0]:
                #         length += len(segs[index])
                #         index += 1
                #     if term != segs[index]:
                #         print term
                #
                # index = 0
                # length = 0
                # for item in n:
                #     term = item[1]
                #     while length < item[0]:
                #         length += len(segs[index])
                #         index += 1
                #     if term != segs[index]:
                #         print term


    # sentences = parseDocx(getXml(path + '1.docx'))
    # for (sentence, pos, neg) in sentences:
    #     segs = segment(sentence)
    #     tagged = [(term.word, term.flag) for term in segs]
    #     for (w, f) in tagged:
    #         if not poses.has_key(f):
    #             poses[f] = {}
    #         if not poses.has_key(w):
    #             poses[f][w] = True

    # pos_array = []
    # for f in poses:
    #     print f, pos_count[f]
    #     pos_array.append((f, list(poses[f])))
    # pos_array.sort(lambda a,b:pos_count[b[0]] - pos_count[a[0]])
    #
    # f = open('../test/static.txt', 'w+')
    # f.write(json.dumps(pos_array, ensure_ascii=False).encode('utf-8'))
    # f.close()


def extract_feature_unigram(sentences):
    sentence = sentences[0]
    pos = sentences[1]
    neg = sentences[2]

    features = []
    count_pos = 0
    count_neg = 0
    terms = []

    for index in range(0, len(sentence)):
        term = sentence[index]
        terms.append(term)

        if index in pos:
            count_pos += 1
        elif index in neg:
            count_neg += 1

        if term in punt_list:
            polar = 'neu'
            if count_pos > count_neg:
                polar = 'pos'
            elif count_neg > count_pos:
                polar = 'neg'
            features.append([terms, polar])
            count_pos = 0
            count_neg = 0
            terms = []

    f = open('../test/unigram.txt', 'w+')
    f.write(json.dumps(features, ensure_ascii=False).encode('utf-8'))
    f.close()
    return features