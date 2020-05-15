# -*- coding: utf-8 -*-
'''
    SSRP演示平台之维普中文期刊爬虫 --- qikan.cqvip.com
    单次页面浏览最多5000条

    测试链接 --- 列表页: http://qikan.cqvip.com/Qikan/Search/Index?from=Qikan_Search_Index
            --- 详情页: http://qikan.cqvip.com/Qikan/Article/Detail?id=7100941916&from=Qikan_Search_Index
'''

import re
import math
import json
import pyexcel
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import urllib.request
import socket
from retry import retry
from settings import *


class CqvipSpider(object):

    def __init__(self):
        self.base_url = 'http://qikan.cqvip.com/Qikan/Search/Index?'
        self.main_url = 'http://qikan.cqvip.com'
        self.test_url = 'http://qikan.cqvip.com/Search/SearchList'
        self.session = HTMLSession()

        com = CommonSettings()
        self.headers = com.set_common_headers()
        self.keyword = com.set_common_keyword()
        self.pagesize = com.set_common_pagesize()
        self.csvname = com.set_common_output()[1]

    @retry()
    def post(self, url, data):
        result = self.session.post(url, data=data, timeout=10)
        result.encoding = result.apparent_encoding
        return result

    def get_init_page(self):
        data = {
            'key': 'U=' + self.keyword,
            'isNoteHistory': '1',
            'isLog': '1',
            'indexKey': self.keyword,
            'indexIdentifier': 'U'
        }
        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:

                result = self.post(self.base_url, data)

                print('status of init page is %s' % result)
                if result.status_code != 200:
                    attempts += 1
                    print('status.error')
                    print('第' + str(attempts) + '次重试！！')
                    if attempts == 50:
                        break
                else:
                    bsoj = BeautifulSoup(result.text, features='lxml')
                    # print(bsoj)
                    total_count = bsoj.find('input', {'id': 'hidShowTotalCount'})['value']
                    page_count = math.ceil(int(total_count)/self.pagesize)
                    print(page_count)

                    socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                    success = True
                    return total_count, page_count

            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('init page callback: %s' % e)
                print('第' + str(attempts) + '次重试！！')
                if attempts == 50:
                    break

    def get_qikan_page(self):
        container = []
        null = None  # python中的None vs js中的Null
        total_count = self.get_init_page()[0]
        page_count = self.get_init_page()[1]
        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                # for page in range(page_count):
                for page in range(1, 2):  # for test
                    searchParamModel = json.dumps({"ObjectType": 1, "SearchKeyList":[],"SearchExpression": null,"BeginYear": null,"EndYear": null,"UpdateTimeType": null,"JournalRange": null,"DomainRange": null,"ClusterFilter": "","ClusterLimit": 0,"ClusterUseType": "Article","UrlParam": "U=" + self.keyword,"Sort": "0","SortField": null,"UserID": "0","PageNum": int(page),"PageSize": self.pagesize,"SType": null,"StrIds": null,"IsRefOrBy": 0,"ShowRules": "  任意字段=" + self.keyword + "  ","IsNoteHistory": 0,"AdvShowTitle": null,"ObjectId": null,"ObjectSearchType": 0,"ChineseEnglishExtend": 0,"SynonymExtend": 0,"ShowTotalCount": int(total_count),"AdvTabGuid":""})
                    # print(searchParamModel)
                    data = {
                        'searchParamModel': searchParamModel
                    }

                    result = self.post(self.test_url, data)
                    print('status of qikan page is %s' % result)

                    if result.status_code != 200:
                        attempts += 1
                        print('qikan.status.error')
                        print('第' + str(attempts) + '次重试！！')
                        if attempts == 50:
                            break
                    else:
                        soup = BeautifulSoup(result.text, features='lxml')
                        # print(soup)
                        simple_div = soup.find('div', {'class': 'simple-list'})
                        dls = simple_div.findAll('dl')
                        for dl in dls:
                            field = {}
                            dt = dl.find('dt')
                            if dt.find('span', {'class': 'cited'}):
                                cited_span = dt.find('span', {'class': 'cited'})
                                cited = cited_span.find('a')['data-zkbycount']
                                field['cited'] = cited
                            else:
                                cited = '0'
                                field['cited'] = cited

                            download = self.main_url + dt.find('a')['href']
                            field['download'] = download

                            container.append(field)

                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
                print(len(container))
                return container

            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('qikan page callback: %s' % e)
                print('第' + str(attempts) + '次重试！！')
                if attempts == 50:
                    break

    def get_detail_page(self):

        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                repos = []
                container = self.get_qikan_page()
                # for contain in container:
                for contain in container[:1]:  # for test
                    repo = {}
                    cited = contain['cited']
                    repo['cited'] = cited
                    download = contain['download']
                    repo['download'] = download
                    print(download)

                    abuyun = AbuyunProxy()
                    proxy_handler = abuyun.urllib_proxy_settings()[1]
                    opener = urllib.request.build_opener(proxy_handler)
                    urllib.request.install_opener(opener)

                    request = urllib.request.Request(download, headers=self.headers)
                    print('status of detail page is %s' % request)
                    html = urllib.request.urlopen(request, timeout=10).read()
                    soup = BeautifulSoup(html, 'lxml')
                    # print('detail page is parsed as \n%s' % soup)
                    title_div = soup.find('div', {'class': 'article-title'})
                    raw_title = title_div.find('h1').get_text()
                    title = re.sub('预览', '', raw_title).strip().replace('\r', '').replace('\n', '')
                    print(title)
                    repo['title'] = title

                    article_div = soup.find('div', {'class': 'article-detail'})
                    abstract_div = article_div.find('div', {'class': 'abstract'})
                    abstract = abstract_div.find('span', {'class': 'abstract'}).get_text().strip('\n').strip('\'')
                    print(abstract)
                    repo['abstract'] = abstract

                    author_div = article_div.find('div', {'class': 'author'})
                    raw_author = author_div.findAll('span')[1].get_text().replace('\n', ',')
                    author = re.sub('^,|,$', '', raw_author)
                    print(author)
                    repo['author'] = author

                    if article_div.find('div', {'class': 'organ'}):
                        info_div = article_div.find('div', {'class': 'organ'})
                        info = info_div.findAll('span')[1].get_text().strip('\n')
                        print(info)
                        repo['info'] = info
                    else:
                        info = 'N/A'
                        repo['info'] = info

                    if article_div.find('div', {'class': 'journal'}):
                        date_div = article_div.find('div', {'class': 'journal'})
                        raw_date = date_div.find('span', {'class': 'vol'}).get_text().strip('\n').strip('\'').strip('').strip()
                        date = re.search('^.*年', raw_date).group()
                        print(date)
                        repo['date'] = date
                    else:
                        date = 'N/A'
                        repo['date'] = date

                    source = '维普期刊'
                    repo['source'] = source

                    downed = '暂无'
                    repo['downed'] = downed

                    if article_div.find('div', {'class': 'fund'}):
                        fund_div = article_div.find('div', {'class': 'fund'})
                        funds = []
                        if len(fund_div.findAll('span')) > 2:
                            fund_span = fund_div.findAll('span')[1:]
                            for span in fund_span:
                                fund_piece = span.get_text()
                                funds.append(fund_piece)
                            fund = ','.join(funds)
                            print(fund)
                            repo['fund'] = fund
                        else:
                            fund = fund_div.findAll('span')[1].get_text()
                            repo['fund'] = fund
                    else:
                        fund = 'N/A'
                        repo['fund'] = fund

                    if article_div.find('div', {'class': 'subject'}):
                        kws_div = article_div.find('div', {'class': 'subject'})
                        kwss = []
                        if len(kws_div.findAll('span')) > 2:
                            kws_span = kws_div.findAll('span')[1:]
                            for span in kws_span:
                                kws_piece = span.get_text()
                                kwss.append(kws_piece)
                            kws = ','.join(kwss)
                            repo['kws'] = kws
                        else:
                            kws = kws_div.findAll('span')[1].get_text()
                            repo['kws'] = kws

                    else:
                        kws = 'N/A'
                        repo['kws'] = kws
                    repos.append(repo)

                print(len(repos))
                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
                return repos

            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('detail page callback: %s' % e)
                print('第' + str(attempts) + '次重试！！')
                if attempts == 50:
                    break

    def save_data(self):
        try:
            csv_data = self.get_detail_page()
            sheet = pyexcel.Sheet()
            for data in csv_data:
                sheet.row += pyexcel.get_sheet(adict=data, transpose_after=True)
            sheet.colnames = ['title', 'author', 'source', 'info', 'date', 'kws', 'cited', 'downed', 'abstract', 'fund', 'download']
            print(sheet)
            sheet.save_as(self.csvname)

        except Exception as e:
            print('404 error!%s' % e)

    def pandas_save_data(self):
        try:
            csv_data = self.get_detail_page()
            dataframe = pd.DataFrame(csv_data)
            print(dataframe)
            dataframe.to_csv(self.csvname, index=False, sep=',', encoding='utf-8')
            print('data saved')

        except Exception as e:
            print('404 error!%s' % e)


if __name__ == '__main__':
    cq = CqvipSpider()
    cq.pandas_save_data()
