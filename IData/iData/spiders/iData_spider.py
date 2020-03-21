# -*- coding: utf-8 -*-
"""
    major configuration for iData spiders
    简单检索
    TODO: 1.cited字段容易丢失
          2. spider的速率比较快，而scrapy操作数据库操作比较慢，导致pipeline中的方法调用较慢，这样当一个变量正在处理的时候，一个新的变量过来，之前的变量的值就会被覆盖，比如pipline的速率是1TPS，而spider的速率是5TPS，那么数据库应该会有5条重复数据

"""
import scrapy
import copy
import re
import math
import random
from urllib import parse
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from iData.items import IdataItem
from scrapy_redis.spiders import RedisCrawlSpider
from iData.user_agent import USER_AGENT
from http import cookiejar


class IDataSpider(RedisCrawlSpider):
    name = 'idata'

    redis_key = "ida_redis"

    kws = '氨基酸'

    maxpage = 5

    def __init__(self,*args, **kwargs):
        self.main_url = 'https://search.cn-ki.net'
        self.search_url = 'https://search.cn-ki.net/search?'
        self.cited_url = 'http://cnki.cn-ki.net/kcms/detail/frame/list.aspx?'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        super(IDataSpider, self).__init__(*args, **kwargs)

    def pre_cookie(self):
        raw_cookies = 'num=zhaobowen9876@163.com; ucks=PpfejJzymT4loE7gnLOF1WGNVHSQi5tC::idata; data=%7B%22ASP.NET_SessionId%22%3A%20%22xrdbfwky4kq5kmd1jk3zti2y%22%2C%20%22SID_kns%22%3A%20%22123119%22%2C%20%22RsPerPage%22%3A%20%2220%22%2C%20%22sort_type%22%3A%20%221%22%2C%20%22query_id%22%3A%20%220%22%2C%20%22Ecp_ClientId%22%3A%20%223200226212405887996%22%7D; session=eyJfcGVybWFuZW50Ijp0cnVlLCJzZWFyY2hfaWQiOnsiIGIiOiJjazFpWnpOMmIzQjVNV1ZWTkVGc1pBPT0ifX0.ETgDBw.IY6QiKq_t52dXvYsI2rXjvLiePk'
        cookie_dict = {}
        items = raw_cookies.split(';')
        for item in items:
            key = item.split('=')[0].strip()
            value = item.split('=')[1]
            cookie_dict[key] = value
        return cookie_dict

    def start_requests(self):
        cookies = self.pre_cookie()
        data = {
                'keyword': self.kws,
                'db': 'CFLS'
        }
        query_string = parse.urlencode(data)
        url = self.search_url + query_string
        yield scrapy.Request(
                             url=url,
                             headers=self.headers,
                             meta={'cookiejar': 1},
                             cookies=cookies,
                             callback=self.parse_page,
                             dont_filter=True
        )

    def parse_page(self,response):
        ida = IdataItem()
        divs = response.xpath('//div[@class="mdui-row mdui-typo"]')
        for d in divs:
            au = d.xpath('.//div/div[1]/span[1]/text()').extract_first()
            if au:
                ida['author'] = au.strip('，')
            else:
                ida['author'] = 'N/A'

            info = d.xpath('.//div/div[1]/span[3]/text()').extract_first()
            if info:
                ida['info'] = info
            else:
                ida['info'] = 'N/A'

            raw_date = d.xpath('.//div/div[1]/span[4]/text()').extract_first()
            if raw_date:
                date = raw_date.strip(' 发表时间：')
                ida['date'] = date
            else:
                ida['date'] = 'N/A'

            source = d.xpath('.//div/div[1]/span[5]/text()').extract_first()
            if source:
                ida['source'] = source
            else:
                ida['source'] = 'N/A'

            detail_link = d.xpath('.//div/h3/a/@href').extract_first() # 详情页
            d_url = self.main_url + '/' + detail_link
            # self.logger.info('detailed page!!!')
            # self.logger.info(d_url)
            yield scrapy.Request(
                                 url=d_url,
                                 headers=self.headers,
                                 meta={'ida_child': copy.deepcopy(ida),
                                       'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_detail_page,
                                 dont_filter=True
            )
        # page_links = response.xpath('//div[@class="mdui-row"]/div/a/@href').extract()  # search?keyword=xx&db=CFLS&p=xx
        # end = response.xpath('//div[@class="mdui-row"]/div/font[@class="Mark"]/text()').extract()
        # if not end:
            # next_link = page_links[-1]
            # next_url = self.main_url + '/' + next_link
            # self.logger.info(next_url)
        # 搜索结果数
        soup = BeautifulSoup(response.text, features="lxml")
        search = soup.find('div', {'class': 'pagerTitleCell'})
        # search = response.xpath('//span[@class="pagerTitle"]/text()').extract_first()

        if search:
            search_res = search.get_text()
        else:
            return 'End'
        tol_num = ''.join(re.findall(r"\d+\.?\d*", search_res))
        page_num = math.ceil(float(tol_num)/20)

        for page in range(2, page_num):
        # for page in range(2, self.maxpage):
            data = {
                'keyword': self.kws,
                'db': 'CFLS',
                'p': page
            }
            query_string = parse.urlencode(data)
            next_url = self.search_url + query_string
            # self.logger.info('next page!!!')
            # self.logger.info(next_url)
            yield scrapy.Request(
                                 url=next_url,
                                 headers=self.headers,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_page,
                                 dont_filter=True
            )
        # else:
            # return 'No next page!'

    def parse_detail_page(self,response):
        ida = response.meta['ida_child']

        ida['title'] = response.xpath('//span[@class="headline"]/text()').extract_first()

        # ***前端页面经过vuetify渲染，无法直接爬取***
        ida['abstract'] = response.xpath('//v-card-text/text()').extract_first().strip()

        down = response.xpath('//v-card-actions/v-btn[1]/@href').extract_first()
        if down:
            ida['download'] = down
        else:
            ida['download'] = 'N/A'

        divs = response.xpath('//v-container[@class="body-1 grey--text text--darken-2"]/v-layout')
        for d in divs:
            flexs = d.xpath("v-flex").extract()

            if re.search("关键词", flexs[0]):
                raw_val = flexs[1].strip('<v-flex xs10 lg11>\n')
                raw_val1 = raw_val.strip('\n                        </v-flex>')
                ida['kws'] = raw_val1
            else:
                ida['kws'] = 'N/A'

            if re.search("基金", flexs[0]):
                raw_val = flexs[1].strip('<v-flex xs10 lg11>\n')
                raw_val1 = raw_val.strip('\n                        </v-flex>')
                ida['fund'] = raw_val1
            else:
                ida['fund'] = 'N/A'

        # **********second attempt************ #
        # 添加cnki-link
        # 获取被引数和下载数
        cnki_url = response.xpath('//v-card-actions/v-spacer/following-sibling::v-btn/@href').extract_first()
        yield scrapy.Request(
                             url=cnki_url,
                             headers=self.headers,
                             meta={'ida_grandchild': copy.deepcopy(ida),
                                    'cookiejar': response.meta['cookiejar']},
                             callback=self.parse_cnki_page,
                             dont_filter=True
        )

    def parse_cnki_page(self,response):
        ida = response.meta['ida_grandchild']
        downed = response.xpath('//div[@class="total"]/span[1]/b/text()').extract_first()

        kws = response.xpath('//label[@id="catalog_KEYWORD"]/following-sibling::a/text()').extract_first()
        kws = kws.strip(';\r\n                  ')
        if ida['kws'] == 'N/A':
            ida['kws'] = kws

        if downed:
            ida['downed'] = downed
        else:
            ida['downed'] = '0'
        # cited 无法直接获取
        # 进入cited详情页

        cur_url = response.url
        query = urlparse(cur_url)
        params = parse_qs(query.query)
        refer_data = {}

        for key in params.keys():
            if key.lower() == 'dbcode':
                refer_data['dbcode'] = ''.join(params[key])  # 得到的value是列表
            if key.lower() == 'dbname':
                refer_data['dbname'] = ''.join(params[key])
            if key.lower() == 'filename':
                refer_data['filename'] = ''.join(params[key])

        refer_data['RefType'] = 3
        refer_data['vl'] = ''
        query_string = parse.urlencode(refer_data)
        cited_url = self.cited_url + query_string
        yield scrapy.http.Request(
                                  url=cited_url,
                                  headers=self.headers,
                                  meta={'ida_lastchild': copy.deepcopy(ida),
                                        'cookiejar': response.meta['cookiejar']},
                                  callback=self.parse_cited_page,
                                  dont_filter=True
        )

    def parse_cited_page(self,response):
        import time
        time.sleep(1)
        ida = response.meta['ida_lastchild']
        count_li = response.xpath('//span[@name="pcount"]/text()').extract()
        num_li = list(map(int, count_li))  # convert to num
        cited = sum(num_li)
        time.sleep(1)
        if cited:
            ida['cited'] = str(cited)
        else:
            ida['cited'] = '0'
        yield ida














