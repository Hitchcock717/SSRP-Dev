import re
import ast
import json
import subprocess
from .utils import ExtractAndRecommend, GetRawResult
from .main import execute_spider

from django.http import QueryDict
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.forms.models import model_to_dict
from .models import Message, Extractor, Recommend, Simplesearch, MessageSerializer, ExtractorSerializer, RecommendSerializer, SimplesearchSerializer


@api_view(('GET',))
def extract(request):

    id_pool = []

    latest = Message.objects.last()
    raw_dict = model_to_dict(latest)
    print(raw_dict)

    serializer_context = {
        'request': request,
    }

    base_router = 'http://127.0.0.1:8000/api/extract/'

    # 查询增量数据
    pre_id = raw_dict['id']  # 历史id
    if pre_id in id_pool:
        id_pool = id_pool
    elif len(id_pool) > 2:
        id_pool.pop(index=0)
        id_pool.append(pre_id)
    else:
        id_pool.append(pre_id)

    extractors = []
    extractors_group = []

    if len(id_pool) < 2:

        ex = ExtractAndRecommend()
        extr_kws = ex.extract_kws(raw_dict)

        for kws in extr_kws:
            extr = Extractor(originkws=kws)
            extr.save()

            # retrieve kws
            data = Extractor.objects.filter(originkws=kws)

            raw_d_dict = []
            for d in data:
                d_dict = model_to_dict(d)
                raw_d_dict.append(d_dict)

            set_only = []
            set_only.append(raw_d_dict[0])

            # drop reqeated
            for item in raw_d_dict:
                k = 0
                for iitem in set_only:
                    if item['originkws'] != iitem['originkws']:
                        k += 1
                    else:
                        break

                    if k == len(set_only):
                        set_only.append(item)

            for only in set_only:
                pkid = only['id']
                extractor = ExtractorSerializer(data=only, context=serializer_context)
                if extractor.is_valid():
                    ordered_li = extractor.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    extractors.append(ordered_li)

        try:
            if extractors is not None:
                extractors.sort(key=lambda x: (x['pk']), reverse=False)
                return Response(extractors)

        except Exception as e:
            return Response('None extracted objects!')

    elif len(id_pool) == 2:
        updates = Message.objects.all()[id_pool[0]:id_pool[1]]
        for update in updates:
            update_dict = model_to_dict(update)
            ex = ExtractAndRecommend()
            extr_kws = ex.extract_kws(update_dict)

            for kws in extr_kws:
                extr = Extractor(originkws=kws)
                extr.save()

                # retrieve kws
                data = Extractor.objects.filter(originkws=kws)

                raw_d_dict = []
                for d in data:
                    d_dict = model_to_dict(d)
                    raw_d_dict.append(d_dict)

                set_only = []
                set_only.append(raw_d_dict[0])

                # drop reqeated
                for item in raw_d_dict:
                    k = 0
                    for iitem in set_only:
                        if item['originkws'] != iitem['originkws']:
                            k += 1
                        else:
                            break

                        if k == len(set_only):
                            set_only.append(item)
                for only in set_only:
                    pkid = only['id']
                    extractor = ExtractorSerializer(data=only, context=serializer_context)
                    if extractor.is_valid():
                        ordered_li = extractor.validated_data
                        ordered_li['pk'] = pkid
                        ordered_li['url'] = base_router + str(pkid) + '/'
                        ordered_li = dict(ordered_li)
                        extractors.append(ordered_li)

                if extractors is not None:
                    extractors.sort(key=lambda x: (x['pk']), reverse=False)
                    extractors_group.extend(extractors)
                else:
                    print('The extractors are empty!')

        try:
            if extractors_group is not None:
                return Response(extractors_group)
        except Exception as e:
            return Response('None extracted objects!')


@api_view(('GET',))
def recommend(request):

    id_pool = []

    latest = Message.objects.last()
    raw_dict = model_to_dict(latest)

    serializer_context = {
        'request': request,
    }

    base_router = 'http://127.0.0.1:8000/api/extract/'

    # 查询增量数据
    pre_id = raw_dict['id']  # 历史id
    if pre_id in id_pool:
        id_pool = id_pool
    elif len(id_pool) > 2:
        id_pool.pop(index=0)
        id_pool.append(pre_id)
    else:
        id_pool.append(pre_id)

    recommends = []
    recommends_group = []

    if len(id_pool) < 2:

        ex = ExtractAndRecommend()
        recom_kws = ex.recommend_kws(raw_dict)

        for rkws in recom_kws:
            recom = Recommend(recommendkws=rkws)
            recom.save()

            # retrieve kws
            data = Recommend.objects.filter(recommendkws=rkws)

            raw_d_dict = []
            for d in data:
                d_dict = model_to_dict(d)
                raw_d_dict.append(d_dict)

            set_only = []
            set_only.append(raw_d_dict[0])

            # drop reqeated
            for item in raw_d_dict:
                k = 0
                for iitem in set_only:
                    if item['recommendkws'] != iitem['recommendkws']:
                        k += 1
                    else:
                        break

                    if k == len(set_only):
                        set_only.append(item)

            for only in set_only:
                pkid = only['id']
                recommend = RecommendSerializer(data=only, context=serializer_context)
                if recommend.is_valid():
                    ordered_li = recommend.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    recommends.append(ordered_li)

        try:
            if recommends is not None:
                recommends.sort(key=lambda x: (x['pk']), reverse=False)
                print(recommends)

                return Response(recommends)
        except Exception as e:
            return Response('None extracted objects!')

    elif len(id_pool) == 2:

        updates = Message.objects.all()[id_pool[0]:id_pool[1]]

        for update in updates:
            update_dict = model_to_dict(update)
            ex = ExtractAndRecommend()
            recom_kws = ex.recommend_kws(update_dict)

            for rkws in recom_kws:
                recom = Recommend(recommendkws=rkws)
                recom.save()

                # retrieve kws
                data = Recommend.objects.filter(recommendkws=rkws)

                raw_d_dict = []
                for d in data:
                    d_dict = model_to_dict(d)
                    raw_d_dict.append(d_dict)

                set_only = []
                set_only.append(raw_d_dict[0])

                # drop reqeated
                for item in raw_d_dict:
                    k = 0
                    for iitem in set_only:
                        if item['recommendkws'] != iitem['recommendkws']:
                            k += 1
                        else:
                            break

                        if k == len(set_only):
                            set_only.append(item)

                for only in set_only:
                    pkid = only['id']
                    recommend = RecommendSerializer(data=only, context=serializer_context)
                    if recommend.is_valid():
                        ordered_li = recommend.validated_data
                        ordered_li['pk'] = pkid
                        ordered_li['url'] = base_router + str(pkid) + '/'
                        ordered_li = dict(ordered_li)
                        recommends.append(ordered_li)

                if recommends is not None:
                    recommends.sort(key=lambda x: (x['pk']), reverse=False)
                    recommends_group.extend(recommends)
                else:
                    print('The recommends are empty!')

        try:
            return Response(recommends_group)
        except Exception as e:
            return Response('None extracted objects!')


@api_view(('POST', 'GET',))
def startspider(request):
    if request.method == 'POST':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        spider_dict = ast.literal_eval(raw_dict_key)
        spider_names = spider_dict['spiders']

        # 转义符处理
        drop_slash_extractors = re.sub('\\\\*', '', spider_dict['extractors'])
        drop_quotation_extractors = re.sub('""', '', drop_slash_extractors)

        drop_slash_recommends = re.sub('\\\\*', '', spider_dict['recommends'])
        drop_quotation_recommends = re.sub('""', '', drop_slash_recommends)

        spider_extractors = ast.literal_eval(drop_quotation_extractors.strip(']['))  # tuple
        spider_recommends = ast.literal_eval(drop_quotation_recommends.strip(']['))
        # extractors_dict = {item['originkws']:item for item in spider_extractors}  # list[dict{}] ---> dict{dict{}}

        extractors = []
        if isinstance(spider_extractors, tuple):
            for extractors_dict in spider_extractors:
                extracted_words = extractors_dict['originkws']
                extractors.append(extracted_words)
        else:
            extracted_words = spider_extractors['originkws']
            extractors.append(extracted_words)

        recommends = []
        if isinstance(spider_recommends, tuple):
            for recommends_dict in spider_recommends:
                recommend_words = recommends_dict['recommendkws']
                recommends.append(recommend_words)
        else:
            recommend_words = spider_recommends['recommendkws']
            recommends.append(recommend_words)

        search_keywords = []
        search_keywords.extend(extractors)
        search_keywords.extend(recommends)

        keywords = list(set(search_keywords))
        print(keywords)

        new_keywords = []

        # 匹配检索表达式1
        if len(keywords) < 2:
            new_keywords.append(keywords[0])
        else:
            for word in keywords[:-2]:
                new_word = word + ' OR '
                new_keywords.append(new_word)
            new_keywords.append(keywords[-1])

        query = ''.join(new_keywords)

        sum_count = 0
        sum_doc = []

        # 爬虫字段存储
        queries = []
        # title, author, source, info, date, kws, fund, abstract, cited, downed, download = [], [], [], [], [], [], [], [], [], [], []
        for word in keywords:
            raw_search_result = GetRawResult()
            # 匹配检索表达式2
            query_body = raw_search_result.get_raw_result(word)[0]  # {}
            queries.append(query_body)

            word_count = raw_search_result.get_raw_result(word)[1]
            sum_count += word_count

            word_doc = raw_search_result.get_raw_result(word)[2]  # [{}]
            sum_doc.extend(word_doc)  # [{}]

        set_only = []
        set_only.append(sum_doc[0])

        # drop reqeated
        for item in sum_doc:
            k = 0
            for iitem in set_only:
                if item['title'] != iitem['title']:
                    k += 1
                else:
                    break

                if k == len(set_only):
                    set_only.append(item)  # [{no repeated}]

        # 过滤后的搜索结果数
        filter_count = len(set_only)

        for each_word_doc in set_only:

            title = each_word_doc['title']
            author = each_word_doc['author']
            source = each_word_doc['source']
            info = each_word_doc['info']
            date = each_word_doc['date']
            kws = each_word_doc['kws']
            fund = each_word_doc['fund']
            abstract = each_word_doc['abstract']
            cited = each_word_doc['cited'].rstrip('.0')
            if cited == 'nan':
                cited = '0'

            downed = each_word_doc['downed'].rstrip('.0')
            if downed == 'nan':
                downed = '0'
            download = each_word_doc['download']

            sim = Simplesearch(title=title, author=author, source=source, info=info, date=date, kws=kws, fund=fund,
                               abstract=abstract, cited=cited, downed=downed, download=download)
            sim.save()

        data = {
            'keywords': keywords,
            'query': queries,
            'raw_search_count': sum_count,
            'filter_search_count': filter_count
        }

        # 暂时指定idata，后续增加引擎
        # for name in spider_names:
            # for word in keywords:
                # execute_spider(name, word)
                # subprocess.check_output(['scrapy', 'crawl', name, '-a', 'keyword='+word])
        return Response(data)

    if request.method == 'GET':
        return Response('No method!')


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ExtractorViewset(viewsets.ModelViewSet):
    queryset = Extractor.objects.all()
    serializer_class = ExtractorSerializer


class RecommedViewset(viewsets.ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer


class SimplesearchViewset(viewsets.ModelViewSet):
    queryset = Simplesearch.objects.all()
    serializer_class = SimplesearchSerializer









