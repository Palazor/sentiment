# -*- coding: utf-8 -*-

import os
import os.path
import zipfile
from lxml import etree
import nltk
nltk.data.path.append('/media/razor/Files/Python27/nltk_data')
from nlpjieba import segment

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
    punt_list = u',.!?:;~，。！？：；～'
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
            sentences.append((sentence, pos, neg))
            pos = []
            neg = []
            sentence = ''
            for i in range(1, numS - 1):
                sentences.append((frags[i], [], []))
                pos = []
                neg = []
            if numS >= 2:
                sentence = frags[numS - 1]

    return sentences


def run_preprocess(path):
    xmlContent = None
    # for parent, dirnames, filenames in os.walk(path):
    #     for filename in filenames:
    #         xmlContent = getXml(path + filename)

    sentences = parseDocx(getXml(path + '1.docx'))
    for (sentence, pos, neg) in sentences:
        print sentence
        for term in pos:
            print 'pos:', term[0], term[1].encode('utf-8')
        for term in neg:
            print 'neg:', term[0], term[1].encode('utf-8')
        segs = segment(sentence)
        print segs