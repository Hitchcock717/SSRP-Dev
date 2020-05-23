# -*- coding: utf-8 -*-
'''
    SSRP分析平台之词云分析 --- 过滤高频关键词
'''

import codecs
import jieba


class CloudAnalysis(object):

    def __init__(self):

        self.stop_path = '/Users/felix_zhao/Desktop/sourcetree_file/SSRP-Dev/IData/IDataSearch/backdoor/corpus/stopwords.txt'
        self.num = 20

    def keyword_count(self, words):
        # 获取高频词
        counts = {}
        for word in words:
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1

        items = list(counts.items())

        items.sort(key=lambda x: x[1], reverse=True)  # key=lambda 元素: 元素[字段索引] 这里表示对元素第二个字段（频次）进行排序

        frequent = []

        for i in range(self.num):
            frequency = {}
            frequency['word'], frequency['count'] = items[i]
            print('{0:<10}{1:>5}'.format(frequency['word'], frequency['count']))
            frequent.append(frequency)

        return frequent

    def title_or_abstract_count(self, words):
        raw_words = ','.join(words)
        cut_words = jieba.lcut(raw_words)
        print(cut_words)
        # 设置停用词
        stopkey = jieba.analyse.set_stop_words('/Users/felix_zhao/Desktop/stopWord.txt')
        print(stopkey)
        # 获取关键词频率
        tags = jieba.analyse.extract_tags(fr, topK=10, withWeight=True)
        for tag in tags:
            print(tag)

        for cut_word in cut_words:
            if len(cut_word) == 1:
                cut_words.remove(cut_word)
            else:
                stops = stop.split('\n')
                print(stops)
                if cut_word in stops:
                    cut_words.remove(cut_word)
                if cut_word in extra:
                    cut_words.remove(cut_word)

        frequent = self.keyword_count(cut_words)
        return frequent


