# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

from pymongo import MongoClient
from scrapy import Item

import copy


'''
# 将爬虫爬取的数据存储搜索服务器中
class ElasticsearchPipline(object):
 
    def process_item(self, item, spider):
        item.save_es()
        return item
'''

'''
# 将数据写入ES
class IdataPipeline(object):

    def process_item(self, item, spider):
        # 对象拷贝，深拷贝
        # asynItem = copy.deepcopy(item)
        item.save()
        return item
'''

'''
class MongoDBPipeline(object):
    def open_spider(item, spider):
        db_url = spider.settings.get('MONGODB_URL', 'mongodb://127.0.0.1:27017')

        db_name = spider.settings.get('MONGODB_DB_NAME', 'ida')
        item.db_client = MongoClient(db_url)
        item.db = item.db_client[db_name]

    # 关闭数据库
    def close_spider(item, spider):
        item.db_client.close()

    # 对数据进行处理
    def process_item(item, item, spider):
        item.insert_db(item)
        return item

    # 插入数据
    def insert_db(item, item):
        if isinstance(item, Item):
            item = dict(item)
        item.db.books.insert(item)
'''

'''
class CsvPipeline(object):
    def __init__(item):
        item.file = open("amino_acid.csv",'w+')
        item.exporter = CsvItemExporter(item.file, 'utf-8')
        item.exporter.start_exporting()

    def close_spider(item,spider):
        item.exporter.finish_exporting()
        item.file.close()

    def process_item(item,item,spider):
        item.exporter.export_item(item)
        return item

'''


class IdataPipeline(object):
    def open_spider(item, spider):
        item.con = sqlite3.connect("ida3.sqlite")  # 链接数据库
        item.cu = item.con.cursor()

    def process_item(item, spider):
        print(spider.name, 'pipelines')
        insert_sql = "insert or replace into ida2 (title, author, info, source, date, kws, fund, abstract, download, cited, downed) " \
                     "values('{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}')".format(
                                                                                                            item['title'],
                                                                                                            item['author'],
                                                                                                            item['info'],
                                                                                                            item['source'],
                                                                                                            item['date'],
                                                                                                            item['kws'],
                                                                                                            item['fund'],
                                                                                                            item['abstract'],
                                                                                                            item['download'],
                                                                                                            item['cited'],
                                                                                                            item['downed']
            )
        print(insert_sql)
        item.cu.execute(insert_sql)
        item.con.commit()
        return item

    def spider_close(item, spider):
        item.con.close()

