#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
    目的：相似词推荐
    方法1.word2vec训练术语库，获取词向量相似度
    Todo: 需获取句级别的语料
'''

import logging
import codecs
from gensim.models import word2vec
from clean_cnki_term import CleanSpiderData


class Similarity(object):

    def __init__(self, raw, file):
        self.clean = CleanSpiderData()
        self.clean.create(raw, file) # 生成原文件

    # 预处理1.读取原文件
    def in_put(self, file):
        fin = codecs.open(file, 'r', encoding='utf-8')
        term = []
        for f in fin.readlines():
            term.append(f)
        term1 = ''.join(term)
        term2 = term1.split(' ')
        return term2

    # 预处理2. 将搜索词加入新的预训练文件
    def preprocess(self, file, file2, kw):
        raw_text = self.in_put(file)
        raw_str = ' '.join(raw_text)
        fout = codecs.open(file2, 'a+', encoding='utf-8')
        fout.write(raw_str)
        fout.write(' '+kw)
        fout.flush()
        fout.close()

    # 方法1.词向量训练
    def main(self, file, file2, kw, path):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        sentences = word2vec.Text8Corpus(file)
        print(file)
        model = word2vec.Word2Vec(sentences, size=150, min_count=1, sg=1)
        # 保存模型，供以后使用
        model.save(path)

        try:
            sim = model.wv.most_similar(kw)
            print(sim)
            return sim

        except KeyError:  # 若搜索词未登录
            self.preprocess(file, file2, kw)
            file3 = file2
            self.main(file3, file2, kw, path)

    def choose(self, file2, kw, path):
        top_ten = self.main(file2,file2,kw,path)  # file——>file2
        print(top_ten)
        recommend = []
        for k_v in top_ten:
            term = k_v[0]
            # score = k_v[1]
            recommend.append(term)
        print(recommend)
        return recommend

    # 方法1.词向量训练其他方式
    def other_methods(self, model):
        print("提供 3 种测试模式\n")
        print("输入一个词，则去寻找前一百个该词的相似词")
        print("输入两个词，则去计算两个词的余弦相似度")
        print("输入三个词，进行类比推理")

        while True:
            try:
                query = input('')
                q_list = query.split()

                if len(q_list) == 1:
                    print("相似词前 100 排序")
                    res = model.most_similar(q_list[0], topn=100)
                    for item in res:
                        print(item[0] + "," + str(item[1]))

                elif len(q_list) == 2:
                    print("计算 Cosine 相似度")
                    res = model.similarity(q_list[0], q_list[1])
                    print(res)
                else:
                    print("%s之于%s，如%s之于" % (q_list[0], q_list[2], q_list[1]))
                    res = model.most_similar([q_list[0], q_list[1]], [q_list[2]], topn=100)
                    for item in res:
                        print(item[0] + "," + str(item[1]))
                print("----------------------------")
            except Exception as e:
                print(repr(e))


if __name__ == "__main__":
    path = '/Users/felix_zhao/Desktop/word2vec.model'
    raw = '/Users/felix_zhao/Desktop/base_data4.txt'
    file = '/Users/felix_zhao/Desktop/base_data4_cn.txt'
    file2 = '/Users/felix_zhao/Desktop/test.txt'
    keyword = '电子显微镜'
    sim = Similarity(raw, file)
    sim.choose(file2, keyword, path)
