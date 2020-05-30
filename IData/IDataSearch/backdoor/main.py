# -*- coding: utf-8 -*-
'''
    SSRP演示平台之爬虫文件导出 + ESjson格式转换 + ES数据插入全流程主运行函数
    tips: 暂时只有cnki爬虫
'''

import sys
import os
import sqlite3
from scrapy.cmdline import execute


# 使用scrapy爬虫时的运行命令(暂时移除)
def execute_spider(name, word):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", name, '-a', 'keyword='+word])


# 主函数
def main():
    es = ESConnect2Data()
    es.execute_spider()
    es.export2csv()
    es.convert2json()
    es.insert2data()


class ESConnect2Data(object):

    # 数据模块自定义设置中心
    def __init__(self):
        # ****** 文件设置 ****** #
        self.sqldb_path = './data/spider_data/spider_data.sqlite'
        self.csv_path = './data/spider_data/spider_data.csv'
        self.json_path = './data/spider_data/doc_json.txt'

        # ****** 数据表设置 ****** #
        self.table_name = 'cnki'

        # ****** ES设置 ****** #
        self.index = 'spider_data'  # new index
        self.ip = '127.0.0.1'

    def execute_spider(self):
        from data.SSRP_CNKIspider import CnkispaceSpider
        CnkispaceSpider().get_candidate_words()
        print('***************** 数据已存入爬虫sqlite数据库! *****************')

    def export2csv(self):
        try:
            import pandas as pd
            con = sqlite3.connect(self.sqldb_path)
            table = pd.read_sql('select * from ' + self.table_name, con)
            table.to_csv(self.csv_path)
            con.close()
            print('***************** 爬虫sqlite数据库已完成文件导出! *****************')
        except Exception as e:
            print(e)

    def convert2json(self):
        from data.ES_doc_convert import ESDocConvert
        ESDocConvert().convert2json(self.csv_path, self.json_path)
        print('***************** 爬虫csv文件已转换成json格式! *****************')

    def insert2data(self):
        from es.ES_insert_data import Insert2ES
        Insert2ES(self.index, self.ip).insert_data(self.json_path)
        print('***************** 爬虫json文件已插入ES中! *****************')


if __name__ == '__main__':
    main()

