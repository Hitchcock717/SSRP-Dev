import os
from .es.ES_kws_retrieve import KeywordRetrieveES
from .es.ES_term_recommend import TermRecommendES


# ******************* 处理关键词 ***************** #


class ExtractAndRecommend(object):

    def __init__(self):
        # ES术语索引地址
        self.index = 'cnki_term_simple'
        self.ip = '127.0.0.1'

        # 词表地址
        os.chdir('/Users/felix_zhao/Desktop/sourcetree_file/SSRP-Dev/IData/IDataSearch/backdoor/corpus')
        self.stop = 'stopwords.txt'
        self.range = 'range_words.txt'

        self.extr_kws = []
        self.recom_kws = []

    def extract_kws(self, raw_dict):

        # extract keywords
        if raw_dict['subject'] == '关键词':
            kwss = raw_dict['body']
            kws_li = kwss.split(',')
            try:
                if kws_li is not None:
                    for kws in kws_li:
                        self.extr_kws.append(kws)
                    return self.extr_kws
            except Exception as e:
                print(e)

        elif raw_dict['subject'] == '标题':
            await_title = raw_dict['body']

            sp = KeywordRetrieveES(self.index, self.ip)
            parsed_sent = sp.parse(await_title)
            parsed_sent1 = [await_title, parsed_sent]
            kws_li = sp.get_all_property(parsed_sent1, self.stop, self.range)
            try:
                if kws_li is not None:
                    for kws in kws_li:
                        self.extr_kws.append(kws)
                    return self.extr_kws
            except Exception as e:
                print(e)

    def recommend_kws(self, raw_dict):
        extr_kws = self.extract_kws(raw_dict)
        # recommed keywords
        for keyword in extr_kws:
            retri = TermRecommendES(self.index, self.ip)
            kws_li = retri.filter(keyword)
            self.recom_kws.extend(kws_li)
            try:
                if self.recom_kws is not None:
                    return self.recom_kws
            except Exception as e:
                print(e)

