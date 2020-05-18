# -*- coding: utf-8 -*-
'''
    SSRP演示平台之CNKI知网空间爬虫 --- www.cnki.com.cn

    测试链接 ---- 列表页: http://search.cnki.com.cn/Search/ListResult?searchType=MultiyTermsSearch&Content=%E6%B0%A8%E5%9F%BA%E9%85%B8&Order=1&page=12
            ---- 详情页: http://www.cnki.com.cn/Article/CJFDTOTAL-HXGY200402006.htm
'''

import re
import csv
import math
import codecs
import socket
from requests_html import HTMLSession
from urllib import parse
from bs4 import BeautifulSoup
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from settings import *


class CnkispaceSpider(object):

    def __init__(self):
        self.base_url = 'http://search.cnki.com.cn/Search/Result?'  # 搜索页
        self.list_url = 'http://search.cnki.com.cn/Search/ListResult?'  # 列表解析页
        self.session = HTMLSession()

        com = CommonSettings()
        self.headers = com.set_common_headers()
        self.keyword = com.set_common_keyword()
        self.pagesize = com.set_common_pagesize()
        self.csvname = com.set_common_output()[0]

    def get_init_page(self):
        data = {
            'searchType': 'MultiyTermsSearch',
            'Content': self.keyword,
            'Order': '1',
            'page': '1'
        }
        query_string = parse.urlencode(data)
        init_url = self.list_url + query_string

        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                abuyun = AbuyunProxy()
                proxy_handler = abuyun.urllib_proxy_settings()[1]
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)

                request = urllib.request.Request(init_url, headers=self.headers)
                # print('status of init page is %s' % request)
                html = urllib.request.urlopen(request, timeout=10).read()
                soup = BeautifulSoup(html, 'lxml')
                total_count = soup.find('input', {'id': 'hidTotalCount'})['value']
                page_count = math.ceil(int(total_count)/self.pagesize)
                # print(page_count)
                success = True
                return page_count

            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('init page callback: %s' % e)
                print("第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break

    def get_detail_page(self):
        page_count = self.get_init_page()
        print('总页数为%s页' % page_count)
        csv_data = []

        breakpoint = 1  # 断点
        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                while breakpoint <= page_count:
                # for i in range(1, 2):  # for test
                    print('正在爬取第%s页...' % breakpoint)
                    data = {
                        'searchType': 'MultiyTermsSearch',
                        'Content': self.keyword,
                        'Order': '1',
                        'page': str(breakpoint)
                    }

                    query_string = parse.urlencode(data)
                    detail_url = self.list_url + query_string

                    abuyun = AbuyunProxy()
                    proxy_handler = abuyun.urllib_proxy_settings()[1]
                    opener = urllib.request.build_opener(proxy_handler)
                    urllib.request.install_opener(opener)

                    request = urllib.request.Request(detail_url, headers=self.headers)
                    # print('status of detail page is %s' % request)
                    html = urllib.request.urlopen(request, timeout=10).read()
                    soup = BeautifulSoup(html, 'lxml')

                    item_divs = soup.findAll('div', {'class': 'list-item'})
                    for item in item_divs:
                        field = []
                        # ****************** 十个公共字段: abstract、info、fund、author、kws、download、title、cited、downed、source **************** #
                        item_p1 = item.find('p', {'class': 'tit clearfix'})
                        title = item_p1.find('a', {'class': 'left'})['title'].replace('\r', '').replace('\n', '')
                        download = item_p1.find('a', {'class': 'left'})['href'].replace('\r', '').replace('\n', '')

                        results = self.get_transfer_page(download)

                        abstract = results[0]
                        info = results[1]
                        fund = results[2]

                        item_p2 = item.find('p', {'class': 'source'})
                        spans = item_p2.findAll('span')
                        author = spans[0]['title'].replace(';', ' ')
                        raw_source = spans[-1].get_text()
                        source = '知网' + raw_source

                        item_p3 = item.find('div', {'class': 'info'})
                        left_p = item_p3.find('p', {'class': 'info_left left'})
                        if len(left_p.findAll('a')) > 0:
                            kws = left_p.find('a')['data-key'].replace(r'/', ';')
                        else:
                            kws = 'N/A'
                        right_p = item_p3.find('p', {'class': 'info_right right'})
                        downed = right_p.find('span', {'class': 'time1'}).get_text().replace('下载', '').strip('（）')
                        cited = right_p.find('span', {'class': 'time2'}).get_text().replace('被引', '').strip('（）')

                        if source == '知网期刊':   # 一个私有字段: date
                            date = spans[2].get_text()

                            field.append(title)
                            field.append(author)
                            field.append(source)
                            field.append(info)
                            field.append(date)
                            field.append(kws)
                            field.append(cited)
                            field.append(downed)
                            field.append(abstract)
                            field.append(fund)
                            field.append(download)
                            csv_data.append(field)

                        elif source == '知网硕士论文' or source == '知网博士论文':  # 一个私有字段: date
                            date = spans[3].get_text()

                            field.append(title)
                            field.append(author)
                            field.append(source)
                            field.append(info)
                            field.append(date)
                            field.append(kws)
                            field.append(cited)
                            field.append(downed)
                            field.append(abstract)
                            field.append(fund)
                            field.append(download)
                            csv_data.append(field)

                    print('第%s页爬取结束!' % breakpoint)
                    breakpoint += 1
                    if breakpoint > page_count:
                        print('已爬取结束, 共%s页' % (breakpoint-1))
                    else:
                        print('新断点记录为第%s页' % breakpoint)

                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
                return csv_data

            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('detail page callback: %s' % e)
                print("第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break

    def get_transfer_page(self, url):

        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                abuyun = AbuyunProxy()
                proxy_handler = abuyun.urllib_proxy_settings()[1]
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)

                request = urllib.request.Request(url, headers=self.headers)
                # print('status of transfer page is %s' % request)
                html = urllib.request.urlopen(request, timeout=10).read()

                soup = BeautifulSoup(html, 'lxml')

                container = []

                if soup.find('div', {'style': 'text-align:left;word-break:break-all'}):
                    abstract = soup.find('div', {'style': 'text-align:left;word-break:break-all'}).get_text().replace(
                        '【摘要】：', '').replace('\r', '').replace('\n', '').strip().replace(',', '，')
                    container.append(abstract)
                else:
                    abstract = 'N/A'
                    container.append(abstract)

                # 期刊
                if soup.find('div', {'style': 'text-align:left;position:relative;'}):
                    other_div = soup.find('div', {'style': 'text-align:left;position:relative;'})
                    other_as = other_div.findAll('a')

                    if len(other_as) == 0:
                        info = 'N/A'
                        fund = 'N/A'
                        container.append(info)
                        container.append(fund)

                    elif len(other_as) == 1:  # 只有作者单位
                        fund = 'N/A'
                        container.append(fund)

                        if other_as[0].get_text():
                            info = other_as[0].get_text()
                            container.append(info)
                        else:
                            info = 'N/A'
                            container.append(info)

                    else:
                        if other_as[0].get_text():
                            info = other_as[0].get_text()
                            container.append(info)
                        else:
                            info = 'N/A'
                            container.append(info)

                        if other_as[1].get_text():
                            fund = other_as[1].get_text().replace(',', '，')
                            container.append(fund)
                        else:
                            fund = 'N/A'
                            container.append(fund)

                elif soup.find('div', {'style': 'text-align:left;'}):
                    other_div = soup.find('div', {'style': 'text-align:left;'}).get_text().split('\n')
                    info = re.sub('【学位级别】.*$', '', other_div[1].replace('【学位授予单位】：', ''))
                    container.append(info)
                    fund = 'N/A'
                    container.append(fund)

                else:  # 如报纸, 跳转至Cnki学问
                    info = 'N/A'
                    fund = 'N/A'
                    container.append(info)
                    container.append(fund)

                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
                return container

            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('transfer page callback: %s' % e)
                print("第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break

    def save_data(self):
        csv_data = self.get_detail_page()
        try:
            with codecs.open(self.csvname, 'w+', encoding='utf-8') as csvfile:
                spamwriter = csv.writer(csvfile, dialect='excel')
                spamwriter.writerow(['title', 'author', 'source', 'info', 'date', 'kws', 'cited', 'downed', 'abstract', 'fund', 'download'])
                spamwriter.writerows(csv_data)
                print('data saved')

        except Exception as e:
            print('404 error!%s' % e)

    def pandas_save_data(self):
        import pandas as pd
        csv_data = self.get_detail_page()
        try:
            columns = ['title', 'author', 'source', 'info', 'date', 'kws', 'cited', 'downed', 'abstract', 'fund', 'download']
            dataframe = pd.DataFrame(csv_data, columns=columns)
            print(dataframe)
            dataframe.to_csv(self.csvname, sep=',', mode='w+', index=False, encoding='utf-8')
            print('data saved')

        except Exception as e:
            print('404 error!%s' % e)


if __name__ == '__main__':
    cnki = CnkispaceSpider()
    cnki.pandas_save_data()

