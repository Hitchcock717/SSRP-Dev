# -*- coding: utf-8 -*-
'''
    SSRP演示平台之万方数据爬虫 --- wanfangdata.com.cn
    单次页面浏览最多2000条

    测试链接 ---- 列表页: http://www.wanfangdata.com.cn/search/searchList.do?searchType=perio&showType=detail&pageSize=20&searchWord=L-%E5%BC%82%E4%BA%AE%E6%B0%A8%E9%85%B8&isTriggerTag=
            ---- 详情页: http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=spyfx202002003
'''

import re
import math
import pyexcel
import pandas as pd
from retry import retry
from urllib import parse
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import urllib.request
import socket
from settings import *


class WFdataspider(object):

    def __init__(self):
        self.base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?'
        self.main_url = 'http://www.wanfangdata.com.cn'
        self.session = HTMLSession()

        com = CommonSettings()
        self.headers = com.set_common_headers()
        self.keyword = com.set_common_keyword()
        self.pagesize = com.set_common_pagesize()
        self.csvname = com.set_common_output()[2]


    @retry()
    def get(self, url, params):
        result = self.session.get(url, params=params, timeout=10)
        return result

    def get_init_page(self):

        data = {
            'searchType': 'all',
            'showType': 'detail',
            'pageSize': str(self.pagesize),
            'searchWord': self.keyword
        }

        query_string = parse.urlencode(data)
        init_url = self.base_url + query_string

        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                result = self.get(init_url, data)
                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
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
                    total_count = bsoj.find('input', {'id': 'resultAnalysisParamFindResults'})['value']
                    page_count = math.ceil(int(total_count)/self.pagesize)
                    # print(page_count)
                    return page_count
            except OSError as e:  # remember to enable proxy connection
                attempts += 1
                print('init page callback: %s' % e)
                print('第' + str(attempts) + '次重试！！')
                if attempts == 50:
                    break

    def get_list_page(self):

        page_count = self.get_init_page()

        repos = []

        # for page in range(page_count):
        for page in range(1, 2):  # for test
            data = {
                   'beetlansyId': 'aysnsearch',
                   'searchType': 'all',
                   'pageSize': '20',
                   'page': page,
                   'searchWord': self.keyword,
                   'order': 'correlation',
                   'showType': 'detail',
                   'isCheck': 'check',
                   'isHit': '',
                   'isHitUnit': '',
                   'firstAuthor': 'false',
                   'corePerio': 'false',
                   'alreadyBuyResource': 'false',
                   'rangeParame': '',
                   'navSearchType': 'all'
                }

            query_string = parse.urlencode(data)
            list_url = self.base_url + query_string

            attempts = 0
            success = False
            while attempts < 50 and not success:
                try:
                    abuyun = AbuyunProxy()
                    proxy_handler = abuyun.urllib_proxy_settings()[1]
                    opener = urllib.request.build_opener(proxy_handler)
                    urllib.request.install_opener(opener)

                    request = urllib.request.Request(list_url, headers=self.headers)
                    print('status of list page is %s' % request)
                    html = urllib.request.urlopen(request, timeout=10).read()
                    soup = BeautifulSoup(html, 'lxml')

                    results = soup.findAll('div', {'class': 'ResultList'})
                    # for res in results:
                    for res in results[:1]:  # for test
                        repo = {}
                        # ****************** 五个公共字段: download、abstract、cited、downed、source **************** #
                        result_div = res.find('div', {'class': 'ResultCont'})
                        title_div = result_div.find('div', {'class': 'title'})
                        suffix = title_div.findAll('a')[0]['href']
                        # 下载链接
                        download = self.main_url + suffix
                        # print(download)
                        repo['download'] = download

                        # 摘要
                        abstract = res.find('div', {'class': 'summary'}).get_text().replace('\r', '').replace('\n', '').strip('"').strip().replace(',', '，')
                        # print(abstract)
                        repo['abstract'] = abstract

                        # 被引数和下载数
                        statistic_div = result_div.find('div', {'class': 'result_new_operaRight result_new_operaItem'})
                        ul_div = statistic_div.find('ul', {'class': 'clear'})
                        ul_as = ul_div.findAll('a')
                        if len(ul_as) == 2:
                            cited = ul_as[0].find('span').get_text()
                            # print(cited)
                            repo['cited'] = cited

                            downed = ul_as[1].find('span').get_text()
                            # print(downed)
                            repo['downed'] = downed

                        elif len(ul_as) == 1:
                            if re.search('被引', ul_as[0].get_text()):
                                cited = ul_as[0].find('span').get_text()
                                # print(cited)
                                repo['cited'] = cited
                                repo['downed'] = 'N/A'

                            elif re.search('下载', ul_as[0].get_text()):
                                downed = ul_as[0].find('span').get_text()
                                # print(downed)
                                repo['cited'] = 'N/A'
                                repo['downed'] = downed

                        else:
                            cited = 'N/A'
                            downed = 'N/A'
                            repo['cited'] = cited
                            repo['downed'] = downed

                        # 出版来源字段 后续统一添加
                        # origin = soup.find('div', {'class': 'Source'}).get_text().strip('》《')
                        # print(origin)

                        # 来源
                        more_info = result_div.find('div', {'class': 'ResultMoreinfo'})
                        author_div = more_info.find('div', {'class': 'author'})
                        raw_source = author_div.find('span', {'class': 'resultResouceType'}).get_text().strip().strip('][')
                        source = '万方' + raw_source
                        # print(source)
                        repo['source'] = source

                        # ****************** private space **************** #
                        if source == '万方期刊论文':  # 六个私有字段: title、kws、info、fund、author、date
                            container = self.get_detail_page(download, source)
                            repo['title'] = container[0]
                            repo['kws'] = container[1]
                            repo['info'] = container[2]
                            repo['fund'] = container[3]

                            author_as = author_div.findAll('a')
                            if len(author_as) > 1:
                                authors = []
                                for au in author_as:
                                    author_piece = au.get_text()
                                    authors.append(author_piece)
                                author = ';'.join(authors)
                                # print(author)
                                repo['author'] = author
                            else:
                                author = author_as[0].get_text()
                                # print(author)
                                repo['author'] = author

                            date_div = soup.find('div', {'class': 'Volume'}).get_text().strip()
                            # print(date_div)
                            date = re.search('^.*年', date_div).group()
                            # print(date)
                            repo['date'] = date
                            repos.append(repo)

                        elif source == '万方专利':  # 六个私有字段: title、kws、author、fund、info、date
                            container = self.get_detail_page(download, source)
                            repo['title'] = container[0]
                            repo['kws'] = container[1]
                            repo['author'] = container[2]
                            repo['fund'] = container[3]

                            source_div = more_info.find('div', {'class': 'Source'})
                            source_spans = source_div.findAll('span')
                            info = source_spans[0].find('a').get_text()
                            # print(info)
                            repo['info'] = info
                            date = source_spans[1].get_text()
                            # print(date)
                            repo['date'] = date
                            repos.append(repo)

                        elif source == '万方硕士论文' or source == '万方博士论文':  # 六个私有字段: title、kws、author、info、date、fund
                            container = self.get_detail_page(download, source)
                            repo['title'] = container[0]
                            repo['kws'] = container[1]
                            repo['author'] = container[2]
                            repo['info'] = container[3]
                            repo['date'] = container[4]
                            repo['fund'] = container[5]
                            repos.append(repo)

                        elif source == '万方会议论文':  # 六个私有字段: title、kws、author、info、date、fund
                            container = self.get_detail_page(download, source)
                            repo['title'] = container[0]
                            repo['kws'] = container[1]
                            repo['author'] = container[2]
                            repo['info'] = container[3]
                            repo['date'] = container[4]
                            repo['fund'] = container[5]
                            repos.append(repo)

                        elif source == '万方科技报告':  # 六个私有字段: title、kws、author、info、date、fund
                            container = self.get_detail_page(download, source)
                            repo['title'] = container[0]
                            repo['kws'] = container[1]
                            repo['author'] = container[2]
                            repo['info'] = container[3]
                            repo['date'] = container[4]
                            repo['fund'] = container[5]
                            repos.append(repo)

                        elif source == '万方成果':  # 六个私有字段: title、kws、author、info、date、fund
                            container = self.get_detail_page(download, source)
                            repo['title'] = container[0]
                            repo['kws'] = container[1]
                            repo['author'] = container[2]
                            repo['info'] = container[3]
                            repo['date'] = container[4]
                            repo['fund'] = container[5]
                            repos.append(repo)

                        else:  # 其他来源 无私有字段
                            repo['title'] = 'N/A'
                            repo['kws'] = 'N/A'
                            repo['author'] = 'N/A'
                            repo['info'] = 'N/A'
                            repo['date'] = 'N/A'
                            repo['fund'] = 'N/A'
                            repos.append(repo)

                    socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                    success = True
                    print(repos)
                    return repos

                except OSError as e:  # remember to enable proxy connection
                    attempts += 1
                    print('list page callback: %s' % e)
                    print('第' + str(attempts) + '次重试！！')
                    if attempts == 50:
                        break

                except AttributeError as e:
                    print(e)

    def get_detail_page(self, url, source):
    # def get_detail_page(self):
        # url = 'http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id=CN201910980511.7'
        # source = '万方专利'

        attempts = 0
        success = False
        while attempts < 50 and not success:
            try:
                abuyun = AbuyunProxy()
                proxy_handler = abuyun.urllib_proxy_settings()[1]
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)

                request = urllib.request.Request(url, headers=self.headers)
                print('status of detail page is %s' % request)
                html = urllib.request.urlopen(request, timeout=10).read()
                soup = BeautifulSoup(html, 'lxml')

                container = []

                raw_title = soup.find('div', {'class': 'title'}).get_text().strip()
                title = re.sub('文摘阅读|下载|第三方链接|被引', '', raw_title).replace('\n', '').replace('\r', '').replace('\t', '')
                container.append(title)

                info_ul = soup.find('ul', {'class': 'info'})
                info_lis = info_ul.findAll('li')

                if source == '万方期刊论文':
                    for info_li in info_lis:
                        if re.search('关键词：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                raw_kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().strip('"').replace('\n', ',')
                                raw_kws1 = re.sub('^,,|,$', '', raw_kws)
                                kws = raw_kws1.replace(',,', ';')
                                # print(kws)
                                container.append(kws)
                            else:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().strip('"').strip()
                                # print(kws)
                                container.append(kws)

                        if re.search('作者单位：', info_li.find('div', {'class': 'info_left'}).get_text()):
                            info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', '').strip(
                            '"').strip().replace(',', '，')
                            print(info)
                            container.append(info)

                        if re.search('基金', info_li.find('div', {'class': 'info_left'}).get_text()):
                            if len(info_li.findAll('a')) > 1:
                                raw_fund = info_li.find('div', {'class': 'info_right author'}).get_text().replace('\r', '').replace('\n', ';').strip().replace(',', '，')
                                fund = re.sub('^;|;$', '', raw_fund)
                                print(fund)
                                container.append(fund)
                            else:
                                fund = info_li.find('div', {'class': 'info_right author'}).get_text().replace('\r', '').replace('\n', '').strip().replace(',', '，')
                                # print(fund)
                                container.append(fund)

                    socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                    success = True
                    return container

                elif source == '万方专利':
                    kws = 'N/A'
                    container.append(kws)
                    for info_li in info_lis:
                        if re.search('发明/设计人：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                raw_author = info_li.find('div', {'class': 'info_right'}).get_text().replace('\n', ',').strip()
                                raw_author1 = re.sub('^,|,,,,,,$', '', raw_author)
                                author = raw_author1.replace(',,,,,,', ';').replace(';', ' ')
                                # print(author)
                                container.append(author)
                            else:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().strip()
                                # print(author)
                                container.append(author)

                        if re.search('专利代理机构：', info_li.get_text()):
                            fund = info_li.find('div', {'class': 'info_right author'}).get_text().replace('\r', '').replace('\n', '').strip().replace(',', '，')
                            # print(fund)
                            container.append(fund)
                        else:
                            fund = 'N/A'
                            container.append(fund)

                elif source == '万方硕士论文' or source == '万方博士论文':
                    for info_li in info_lis:
                        if re.search('关键词：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace(
                                '"\n', ';').strip('"').strip()
                                # print(kws)
                                container.append(kws)
                            else:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().strip('"').strip()
                                # print(kws)
                                container.append(kws)

                        if re.search('作者：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().replace(
                                '"\n', ';').strip('"').strip().replace(';', ' ')
                                # print(author)
                                container.append(author)
                            else:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().strip('"').strip()
                                # print(author)
                                container.append(author)

                        if re.search('学位授予单位：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', ';').strip('"').strip()
                                # print(info)
                                container.append(info)
                            else:
                                info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', '').strip('"').strip()
                                # print(info)
                                container.append(info)

                        if re.search('学位年度：', info_li.get_text()):
                            date = info_li.find('div', {'class': 'info_right author'}).get_text()
                            # print(date)
                            container.append(date)

                        fund = 'N/A'
                        container.append(fund)

                elif source == '万方会议论文':
                    for info_li in info_lis:
                        if re.search('关键词：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace(
                                '"\n', ';').strip('"').strip()
                                # print(kws)
                                container.append(kws)
                            else:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().strip('"').strip()
                                # print(kws)
                                container.append(kws)

                        if re.search('作者：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().replace(
                                '"\n', ';').strip('"').strip().replace(';', ' ')
                                # print(author)
                                container.append(author)
                            else:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().strip('"').strip()
                                # print(author)
                                container.append(author)

                        if re.search('作者单位：', info_li.get_text()):
                            info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', '').strip(
                            '"').strip()
                            # print(info)
                            container.append(info)

                        if re.search('会议时间：', info_li.get_text()):
                            date = info_li.find('div', {'class': 'info_right'}).get_text().strip()
                            # print(date)
                            container.append(date)

                        fund = 'N/A'
                        container.append(fund)

                elif source == '万方科技报告':
                    for info_li in info_lis:
                        if re.search('关键词：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace(
                                '"\n', ';').strip('"').strip()
                                # print(kws)
                                container.append(kws)
                            else:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().strip('"').strip()
                                # print(kws)
                                container.append(kws)

                        if re.search('作者：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().replace(
                                '"\n', ';').strip('"').strip().replace(';', ' ')
                                # print(author)
                                container.append(author)
                            else:
                                author = info_li.find('div', {'class': 'info_right'}).get_text().strip('"').strip()
                                # print(author)
                                container.append(author)

                        if re.search('作者单位：', info_li.get_text()):
                            info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', '').strip(
                            '"').strip()
                            # print(info)
                            container.append(info)

                        if re.search('立项批准年：', info_li.get_text()):
                            date = info_li.find('div', {'class': 'info_right'}).get_text().strip()
                            # print(date)
                            container.append(date)

                        if re.search('计划名称：', info_li.get_text()):
                            fund = info_li.find('div', {'class': 'info_right author'}).get_text().replace('\r', '').replace('\n', '').strip().replace(',', '，')
                            # print(fund)
                            container.append(fund)

                elif source == '万方成果':
                    for info_li in info_lis:
                        if re.search('关键词：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                kws = info_li.find('div',
                                                   {'class': 'info_right info_right_newline'}).get_text().replace(
                                    '"\n', ';').strip('"').strip()
                                # print(kws)
                                container.append(kws)
                            else:
                                kws = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().strip(
                                    '"').strip()
                                # print(kws)
                                container.append(kws)

                        author = 'N/A'
                        container.append(author)

                        if re.search('完成单位：', info_li.get_text()):
                            if len(info_li.findAll('a')) > 1:
                                info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', ';').strip('"').strip()
                                # print(info)
                                container.append(info)
                            else:
                                info = info_li.find('div', {'class': 'info_right info_right_newline'}).get_text().replace('\r', '').replace('\n', '').strip('"').strip()
                                # print(info)
                                container.append(info)

                        if re.search('公布年份：', info_li.get_text()):
                            date = info_li.find('div', {'class': 'info_right author'}).get_text().strip()
                            # print(date)
                            container.append(date)

                        fund = 'N/A'
                        container.append(fund)

                socket.setdefaulttimeout(10)  # 设置10秒后连接超时
                success = True
                return container

            except OSError as e:
                attempts += 1
                print('detail page callback: %s' % e)
                print("第" + str(attempts) + "次重试！！")
                if attempts == 50:
                    break

    def save_data(self):
        try:
            csv_data = self.get_list_page()
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
            csv_data = self.get_list_page()
            dataframe = pd.DataFrame(csv_data)
            print(dataframe)
            dataframe.to_csv(self.csvname, index=False, sep=',', encoding='utf-8')
            print('data saved')

        except Exception as e:
            print('404 error!%s' % e)


if __name__ == '__main__':
    wf = WFdataspider()
    wf.pandas_save_data()
