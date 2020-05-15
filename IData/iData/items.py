# -*- coding: utf-8 -*-

# Define here the models for your scraped selfs
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/selfs.html

# from scrapy_djangoitem import DjangoItem
# from backdoor.models import Idata


# class IdataItem(DjangoItem):
    # django_model = Idata




from .spiders.es_models import IdataSpider
from elasticsearch_dsl.connections import connections
es = connections.create_connection(hosts=['127.0.0.1'])


# 将建立的字段进行分词处理
# *args 元组 **args字典


def conduct_suggest(index, *args):
    """
    :param index: 操作的数据库
    :param args: 需要进行分词的内容
    :return: 返回分词之后的列表
    """
    # 声明空集合
    use_words = set()
    # 声明列表
    suggest = []
    # 分词的分重
    for text, weight in args:
        # 调用分词接口
        words = es.indices.analyze(
            index=index,
            params={
                'filter': ['lowercase']
            },
            body={
                'analyzer': 'ik_max_word',
                'text': text
            }
        )
        analyzer_word = set([x['token'] for x in words['tokens']])
        print(analyzer_word)
        # 计算差集
        new_words = analyzer_word - use_words
        # 加入suggest之前,这条数据在suggest是不存在的
        suggest.append({'input': list(new_words), 'weight': weight})
        use_words = analyzer_word
    # suggest是没有重复数据的
    # [{'input':['土豆','豆','逆','袭'],'weight':10},{'words':['天蚕'],'weight':8}]
    return suggest


import scrapy


class IdataItem(scrapy.Item):
    d_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    info = scrapy.Field()
    date = scrapy.Field()
    kws = scrapy.Field()
    cited = scrapy.Field()
    downed = scrapy.Field()
    download = scrapy.Field()
    abstract = scrapy.Field()
    fund = scrapy.Field()

    """
    # 将数据保存到es搜索服务器中
    def save_es(self):
        idata = IdataSpider()
        # 从传递进来的item中取值
        idata.d_url = self['d_url']
        idata.title = self['title']
        idata.author = self['author']
        idata.source = self['source']
        idata.info = self['info']
        idata.date = self['date']
        idata.kws = self['kws']
        idata.cited = self['cited']
        idata.downed = self['downed']
        idata.download = self['download']
        idata.abstract = self['abstract']
        idata.fund = self['fund']
        # 将数据对应分词信息进行保存
        # 将某些字段进行分词处理, 将处理后的数据保存到suggest中
        idata.suggest = conduct_suggest('idata_doc', (idata.kws,10), (idata.title,8))
        idata.save()
    """


