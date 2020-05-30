# -*- coding: utf-8 -*-
'''
    SSRP推荐平台之获取公共推荐数据
'''

from es.ES_doc_retrieve import DocRetireveES

# ******************* 获取推荐数据 ***************** #


class GetRecommendResult(object):

    def __init__(self):
        # ES文档索引地址
        self.index = 'spider_data'  # 预先存储，后续更改index
        self.ip = '127.0.0.1'
        self.region = '氨基酸'  # 暂定推荐领域

    def get_recom_result(self, multi_kws):
        doc = DocRetireveES(self.index, self.ip)
        multi_fields = ['abstract', 'kws', 'title', 'info', 'fund', 'source']  # 查询所有包含kws的字段
        results = doc.basic_search(multi_fields, multi_kws)
        query = results[0]
        counts = results[1]
        docs = results[2]
        return query, counts, docs

    def drop_duplicates(self, recommend):
        import operator
        for i in recommend:
            for j in recommend:
                if operator.eq(i,j):
                    recommend.remove(i)
                else:
                    continue
        return recommend
