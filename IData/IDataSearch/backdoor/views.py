import re
import ast
import json
import pickle
import subprocess
from .utils import ExtractAndRecommend, GetRawResult, GetDetailResult
from .main import execute_spider

from django.http import QueryDict
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from django.forms.models import model_to_dict
from django.core.cache import caches
from .models import Message, Extractor, Recommend, Simplesearch, Detailsearch, Temp, Folder, Collection, Repository, Corpus, MessageSerializer, ExtractorSerializer, RecommendSerializer, SimplesearchSerializer, DetailsearchSerializer, TempSerializer, FolderSerializer, CollectionSerializer, RepositorySerializer, CorpusSerializer


@api_view(('GET',))
def extract(request):

    latest = Message.objects.last()
    raw_dict = model_to_dict(latest)
    print(raw_dict)

    serializer_context = {
        'request': request,
    }

    base_router = 'http://127.0.0.1:8000/api/extract/'

    extractors = []
    extractors_group = []

    db = 'extractor'
    raw_temps = Temp.objects.filter(record_db=db)
    print(raw_temps)

    if raw_temps:
        temps = []
        for raw_temp in raw_temps:  # 最新的extractor id
            raw_temp_dict = model_to_dict(raw_temp)
            temps.append(raw_temp_dict)
        temp_dict = temps[-1]
        print(temp_dict)
        pre_id = temp_dict['record_id']
        post_id = raw_dict['id']  # 更新id
        temp = Temp(record_id=post_id, record_db=db)
        temp.save()

        updates = Message.objects.filter(id__gt=pre_id)
        print(updates)
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
                    extractors.clear()
                else:
                    print('The extractors are empty!')

        try:
            if extractors_group is not None:
                print(extractors_group)
                return Response(extractors_group)
        except Exception as e:
            return Response('None extracted objects!')

    else:
        pre_id = raw_dict['id']
        print(pre_id)
        temp = Temp(record_id=pre_id, record_db=db)
        temp.save()

        updates = Message.objects.all()
        print(updates)
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
                    extractors.clear()
                else:
                    print('The extractors are empty!')

        try:
            if extractors_group is not None:
                print(extractors_group)
                return Response(extractors_group)
        except Exception as e:
            return Response('None extracted objects!')


@api_view(('GET',))
def recommend(request):

    latest = Message.objects.last()
    raw_dict = model_to_dict(latest)

    serializer_context = {
        'request': request,
    }

    base_router = 'http://127.0.0.1:8000/api/recommend/'

    recommends = []
    recommends_group = []

    db = 'recommend'
    raw_temps = Temp.objects.filter(record_db=db)

    if raw_temps:
        temps = []
        for raw_temp in raw_temps:
            raw_temp_dict = model_to_dict(raw_temp)
            temps.append(raw_temp_dict)
        temp_dict = temps[-1]
        pre_id = temp_dict['record_id']
        post_id = raw_dict['id']
        temp = Temp(record_id=post_id, record_db=db)
        temp.save()

        updates = Message.objects.filter(id__gt=pre_id)
        print(updates)
        for update in updates:
            update_dict = model_to_dict(update)

            ex = ExtractAndRecommend()
            recom_kws = ex.recommend_kws(update_dict)

            try:
                if recom_kws:
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

                        if recommends:
                            recommends.sort(key=lambda x: (x['pk']), reverse=False)
                            recommends_group.extend(recommends)
                            recommends.clear()
                        else:
                            print('The recommends are empty!')
            except Exception as e:
                return Response(['暂无推荐'])

        try:
            return Response(recommends_group)
        except Exception as e:
            return Response(['暂无推荐'])

    else:
        pre_id = raw_dict['id']
        print(pre_id)
        temp = Temp(record_id=pre_id, record_db=db)
        temp.save()

        updates = Message.objects.all()
        print(updates)
        for update in updates:
            update_dict = model_to_dict(update)
            ex = ExtractAndRecommend()
            recom_kws = ex.recommend_kws(update_dict)

            try:
                if recom_kws:
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
                            recommends.clear()
                        else:
                            print('The recommends are empty!')
            except Exception as e:
                return Response(['暂无推荐'])

        try:
            return Response(recommends_group)
        except Exception as e:
            return Response(['暂无推荐'])


@api_view(('POST', 'GET',))
def startspider(request):
    if request.method == 'POST':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        spider_dict = ast.literal_eval(raw_dict_key)
        print(spider_dict)
        spider_names = spider_dict['spiders']

        # 转义符处理
        drop_slash_extractors = re.sub('\\\\*', '', spider_dict['extractors'])
        drop_quotation_extractors = re.sub('^"|"$', '', drop_slash_extractors)
        print(drop_quotation_extractors)

        drop_slash_recommends = re.sub('\\\\*', '', spider_dict['recommends'])
        drop_quotation_recommends = re.sub('^"|"$', '', drop_slash_recommends)
        print(drop_quotation_recommends)

        spider_extractors = ast.literal_eval(drop_quotation_extractors.strip(']['))  # tuple
        print(spider_extractors)
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
        queries = []  # 结构复杂，前台暂无法解析 --- {'query': {'multi_match': {'query': '氨基酸', 'fields': ['abstract', 'kws', 'title', 'info', 'fund', 'source']}}}
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
            if re.search(';', author):
                author = re.sub(';', '', author)
            source = each_word_doc['source']
            info = each_word_doc['info']
            date = each_word_doc['date']
            kws = each_word_doc['kws']
            if kws == 'nan':
                kws = '暂无'
            fund = each_word_doc['fund']
            if fund == 'nan':
                fund = '暂无'
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
            'query': query,
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


@api_view(('GET',))
def rawresult(request):
    if request.method == 'GET':

        latest = Simplesearch.objects.last()
        raw_dict = model_to_dict(latest)

        db = 'rawresult'
        raw_temps = Temp.objects.filter(record_db=db)

        if raw_temps:
            temps = []
            for raw_temp in raw_temps:
                raw_temp_dict = model_to_dict(raw_temp)
                temps.append(raw_temp_dict)
            temp_dict = temps[-1]
            pre_id = temp_dict['record_id']
            post_id = raw_dict['id']
            temp = Temp(record_id=post_id, record_db=db)
            temp.save()

            updates = Simplesearch.objects.filter(id__gt=pre_id)
            # updates = Simplesearch.objects.all()[:50]  # for test

            rawresults = []
            # 自增序号刷新【前端改】
            # uid = 1
            for update in updates:
                update_dict = model_to_dict(update)
                # update_dict['id'] = str(uid)
                # uid += 1

                rawresults.append(update_dict)

            if rawresults is not None:
                print(rawresults)
                return Response(rawresults)
            else:
                return Response('No suitable data!')

        else:
            pre_id = raw_dict['id']
            print(pre_id)
            temp = Temp(record_id=pre_id, record_db=db)
            temp.save()

            updates = Simplesearch.objects.all()
            # updates = Simplesearch.objects.all()[:20]  # for test

            rawresults = []
            # 自增序号刷新【前端改】
            # uid = 1
            for update in updates:
                update_dict = model_to_dict(update)
                # update_dict['id'] = str(uid)
                # uid += 1

                rawresults.append(update_dict)

            if rawresults is not None:
                print(rawresults)
                return Response(rawresults)
            else:
                return Response('No suitable data!')


@api_view(('POST',))
def selectedrawresult(request):
    if request.method == 'POST':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        target_dict = ast.literal_eval(raw_dict_key)
        target_id = int(target_dict['target'].strip('"'))

        # 按对应id查找
        target_data = Simplesearch.objects.filter(id=target_id)
        for data in target_data:
            clean_data = model_to_dict(data)

            return Response(clean_data)

    if request.method == 'GET':
        return Response('No method!')


@api_view(('POST', 'GET',))
def getexpression(request):

    if request.method == 'POST':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        expression_dict = ast.literal_eval(raw_dict_key)
        print(expression_dict)

        raw_expression_body = expression_dict['expression']
        expression_body = ast.literal_eval(raw_expression_body.strip(']['))

        # 有无日期筛选
        expression_date = expression_body[-1]
        start_date = expression_date['startdate']
        end_date = expression_date['endate']

        # 无有效日期
        if start_date == 'null' or end_date == 'null':
            # (1).有且仅有一个表达式
            if len(expression_body) == 2 and expression_body[0]['regex'] == '否':
                expression_context = expression_body[0]

                # 转换成ES中的字段
                if expression_context['type'] == '标题':
                    expression_context['type'] = 'title'
                elif expression_context['type'] == '作者':
                    expression_context['type'] = 'author'
                elif expression_context['type'] == '来源':
                    expression_context['type'] = 'source'
                elif expression_context['type'] == '机构/单位':
                    expression_context['type'] = 'info'
                elif expression_context['type'] == '基金':
                    expression_context['type'] = 'fund'
                elif expression_context['type'] == '关键词':
                    expression_context['type'] = 'kws'
                elif expression_context['type'] == '摘要':
                    expression_context['type'] = 'abstract'

                # 1.1.有且仅有必填项 无正则
                expression_type = expression_context['type']
                expression_info = expression_context['info']

                detail = GetDetailResult()
                results = detail.get_only_expression(expression_type, expression_info)

                sum_doc = results[2]
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

                # 清洗字段
                for each_word_doc in set_only:

                    title = each_word_doc['title']
                    author = each_word_doc['author']
                    source = each_word_doc['source']
                    info = each_word_doc['info']
                    date = each_word_doc['date']
                    kws = each_word_doc['kws']
                    if kws == 'nan':
                        kws = '暂无'
                    fund = each_word_doc['fund']
                    if fund == 'nan':
                        fund = '暂无'
                    abstract = each_word_doc['abstract']
                    cited = each_word_doc['cited'].rstrip('.0')
                    if cited == 'nan':
                        cited = '0'

                    downed = each_word_doc['downed'].rstrip('.0')
                    if downed == 'nan':
                        downed = '0'
                    download = each_word_doc['download']

                    det = Detailsearch(title=title, author=author, source=source, info=info, date=date, kws=kws,
                                       fund=fund, abstract=abstract, cited=cited, downed=downed, download=download)
                    det.save()

                data = {
                    'query': results[0],
                    'raw_count': results[1],
                    'filter_search_count': filter_count,
                    'doc': sum_doc
                }
                print(data)
                return Response(data)

    if request.method == 'GET':
        return Response('No method!')


@api_view(('GET',))
def filteresult(request):
    if request.method == 'GET':

        latest = Detailsearch.objects.last()
        raw_dict = model_to_dict(latest)

        db = 'filteresult'
        raw_temps = Temp.objects.filter(record_db=db)

        if raw_temps:
            temps = []
            for raw_temp in raw_temps:
                raw_temp_dict = model_to_dict(raw_temp)
                temps.append(raw_temp_dict)
            temp_dict = temps[-1]
            pre_id = temp_dict['record_id']
            post_id = raw_dict['id']
            temp = Temp(record_id=post_id, record_db=db)
            temp.save()

            filteresults = []

            updates = Detailsearch.objects.filter(id__gt=pre_id)
            # updates = Detailsearch.objects.all()[:5]  # for test

            # 自增序号刷新
            uid = 1
            for update in updates:
                update_dict = model_to_dict(update)
                update_dict['id'] = str(uid)
                uid += 1

                filteresults.append(update_dict)

            if filteresults is not None:
                print(filteresults)
                return Response(filteresults)
            else:
                return Response('No suitable data!')

        else:
            pre_id = raw_dict['id']
            print(pre_id)
            temp = Temp(record_id=pre_id, record_db=db)
            temp.save()

            filteresults = []
            updates = Detailsearch.objects.all()
            # updates = Detailsearch.objects.all()[:5]  # for test

            # 自增序号刷新
            uid = 1
            for update in updates:
                update_dict = model_to_dict(update)
                update_dict['id'] = str(uid)
                uid += 1

                filteresults.append(update_dict)

            if filteresults:
                print(filteresults)
                return Response(filteresults)
            else:
                return Response('No suitable data!')


@api_view(('POST','GET',))
def getcollection(request):
    if request.method == 'POST':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/collection/'

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        print(raw_dict)
        raw_dict_key = list(raw_dict.keys())[0]
        collection_dict = ast.literal_eval(raw_dict_key)
        print(collection_dict)

        # 收藏词表
        collection = collection_dict['collection'].strip('"')

        collections = []

        if Collection.objects.filter(folder=collection):
            data = Collection.objects.filter(folder=collection)

            raw_d_dict = []
            for d in data:
                d_dict = model_to_dict(d)
                print(d_dict)
                raw_d_dict.append(d_dict)

            set_only = []
            set_only.append(raw_d_dict[0])

            # drop reqeated
            for item in raw_d_dict:
                k = 0
                for iitem in set_only:
                    if item['title'] != iitem['title'] and item['author'] != iitem['author']:
                        k += 1
                    else:
                        break

                    if k == len(set_only):
                        set_only.append(item)

            for only in set_only:
                print(only)
                pkid = only['id']
                collection_data = CollectionSerializer(data=only, context=serializer_context)
                if collection_data.is_valid():
                    ordered_li = collection_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    collections.append(ordered_li)
            print(collections)

            return Response(collections)

        else:
            return Response('failed')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('POST','GET',))
def addcollection(request):
    if request.method == 'POST':

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        print(raw_dict)
        raw_dict_key = list(raw_dict.keys())[0]
        collection_dict = ast.literal_eval(raw_dict_key)
        print(collection_dict)

        # 接口数据
        raw_collected_data = collection_dict['collect']
        flag = collection_dict['flag'].strip('"')
        folder = collection_dict['folder'].strip('"')

        drop_quotation_data = re.sub('^"|"$', '', raw_collected_data)
        collected_data = ast.literal_eval(drop_quotation_data.strip(']['))

        # 收藏论文字段
        title = collected_data['title']
        author = collected_data['author']
        info = collected_data['info']
        date = collected_data['date']

        if not Collection.objects.filter(title=title, author=author, info=info, date=date, flag=flag, folder=folder):
            collect = Collection(title=title, author=author, info=info, date=date, flag=flag, folder=folder)
            collect.save()
            return Response('success')

        else:
            return Response('failed')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('DELETE','GET',))
def deletecollection(request):
    if request.method == 'DELETE':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        collection_dict = ast.literal_eval(raw_dict_key)

        delete_id = collection_dict['delid']
        print(delete_id)

        if not delete_id:
            return Response('failed')
        else:
            get_object_or_404(Collection, pk=int(delete_id)).delete()
        return Response('success')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('POST','GET',))
def getcorpus(request):
    if request.method == 'POST':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/corpus/'

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        print(raw_dict)
        raw_dict_key = list(raw_dict.keys())[0]
        corpus_dict = ast.literal_eval(raw_dict_key)
        print(corpus_dict)

        # 收藏词表
        corpus = corpus_dict['corpus'].strip('"')

        corpuss = []

        if Corpus.objects.filter(repository=corpus):
            data = Corpus.objects.filter(repository=corpus)

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
                    if item['kws'] != iitem['kws']:
                        k += 1
                    else:
                        break

                    if k == len(set_only):
                        set_only.append(item)

            for only in set_only:
                pkid = only['id']
                corpus_data = CorpusSerializer(data=only, context=serializer_context)
                if corpus_data.is_valid():
                    ordered_li = corpus_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    corpuss.append(ordered_li)
            print(corpuss)

            return Response(corpuss)

        else:
            return Response('failed')

    if request.method == 'GET':
        return Response('No method!')


# 添加词汇方式1. 详情页点击收藏
@api_view(('POST','GET',))
def appendcorpus(request):
    if request.method == 'POST':

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        print(raw_dict)
        raw_dict_key = list(raw_dict.keys())[0]
        corpus_dict = ast.literal_eval(raw_dict_key)
        print(corpus_dict)

        # 接口数据
        raw_corpus_data = corpus_dict['corpus']
        repo = corpus_dict['repository'].strip('"')

        print(raw_corpus_data)
        print(repo)

        if not Corpus.objects.filter(kws=raw_corpus_data, repository=repo):
            corp = Corpus(kws=raw_corpus_data, repository=repo)
            corp.save()
            return Response('success')

        else:
            return Response('failed')

    if request.method == 'GET':
        return Response('No method!')


# 添加词汇方式2. 词表库内直接添加
@api_view(('POST','GET',))
def addcorpus(request):
    if request.method == 'POST':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/corpus/'

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        corpus_dict = ast.literal_eval(raw_dict_key)
        print(corpus_dict)

        # 词汇名称
        kws = corpus_dict['kws']
        print(kws)

        corpus = corpus_dict['corpus'].strip('"')
        print(corpus)

        corpuss = []
        # 重复值判断
        if Corpus.objects.filter(kws=kws):
            return Response('failed')
        else:
            corp = Corpus(kws=kws, repository=corpus)
            corp.save()

            data = Corpus.objects.filter(kws=kws, repository=corpus)
            print(data)
            for d in data:
                raw_dict = model_to_dict(d)

                pkid = raw_dict['id']
                corpus_data = CorpusSerializer(data=raw_dict, context=serializer_context)
                if corpus_data.is_valid():
                    ordered_li = corpus_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    corpuss.append(ordered_li)
                    print(ordered_li)

        return Response(corpuss[0])

    if request.method == 'GET':
        return Response('No method!')


@api_view(('DELETE','GET',))
def deletecorpus(request):
    if request.method == 'DELETE':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        corpus_dict = ast.literal_eval(raw_dict_key)

        delete_id = corpus_dict['delid']
        print(delete_id)

        if not delete_id:
            return Response('failed')
        else:
            get_object_or_404(Corpus, pk=int(delete_id)).delete()
        return Response('success')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('GET',))
def getfolder(request):
    if request.method == 'GET':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/folder/'

        data = Folder.objects.all()

        folders = []
        if data:
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
                    if item['folder'] != iitem['folder']:
                        k += 1
                    else:
                        break

                    if k == len(set_only):
                        set_only.append(item)

            for only in set_only:
                pkid = only['id']
                folder_data = FolderSerializer(data=only, context=serializer_context)
                if folder_data.is_valid():
                    ordered_li = folder_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    folders.append(ordered_li)
            print(folders)

            return Response(folders)

        else:
            return Response('failed')


@api_view(('POST','GET',))
def addfolder(request):
    if request.method == 'POST':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/folder/'

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        folder_dict = ast.literal_eval(raw_dict_key)
        print(folder_dict)

        # 收藏夹名称
        fold_name = folder_dict['foldername']
        print(fold_name)

        folders = []

        if not Folder.objects.filter(folder=fold_name):  # 未找到重复值, 先存再取
            folder = Folder(folder=fold_name)
            folder.save()

            data = Folder.objects.filter(folder=fold_name)

            for d in data:
                raw_dict = model_to_dict(d)

                pkid = raw_dict['id']
                corpus_data = FolderSerializer(data=raw_dict, context=serializer_context)
                if corpus_data.is_valid():
                    ordered_li = corpus_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    folders.append(ordered_li)
            print(folders)

            return Response(folders[0])

        else:
            return Response('failed')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('DELETE','GET',))
def deletefolder(request):
    if request.method == 'DELETE':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        folder_dict = ast.literal_eval(raw_dict_key)

        delete_id = folder_dict['delid']
        print(delete_id)

        if not delete_id:
            return Response('failed')
        else:
            get_object_or_404(Folder, pk=int(delete_id)).delete()
        return Response('success')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('GET',))
def getrepository(request):
    if request.method == 'GET':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/repository/'

        data = Repository.objects.all()

        repositorys = []

        if data:
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
                    if item['repository'] != iitem['repository']:
                        k += 1
                    else:
                        break

                    if k == len(set_only):
                        set_only.append(item)

            for only in set_only:
                pkid = only['id']
                repository_data = RepositorySerializer(data=only, context=serializer_context)
                if repository_data.is_valid():
                    ordered_li = repository_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    repositorys.append(ordered_li)
            print(repositorys)

            return Response(repositorys)

        else:
            return Response('failed')


@api_view(('POST','GET',))
def addrepository(request):
    if request.method == 'POST':

        serializer_context = {
            'request': request,
        }

        base_router = 'http://127.0.0.1:8000/api/repository/'

        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        repository_dict = ast.literal_eval(raw_dict_key)
        print(repository_dict)

        # 词表库名称
        repo_name = repository_dict['reponame']
        print(repo_name)

        repos = []

        if not Repository.objects.filter(repository=repo_name):
            repository = Repository(repository=repo_name)
            repository.save()

            data = Repository.objects.filter(repository=repo_name)

            for d in data:
                raw_dict = model_to_dict(d)

                pkid = raw_dict['id']
                corpus_data = RepositorySerializer(data=raw_dict, context=serializer_context)
                if corpus_data.is_valid():
                    ordered_li = corpus_data.validated_data
                    ordered_li['pk'] = pkid
                    ordered_li['url'] = base_router + str(pkid) + '/'
                    ordered_li = dict(ordered_li)
                    repos.append(ordered_li)
            print(repos)

            return Response(repos[0])

        else:
            return Response('failed')

    if request.method == 'GET':
        return Response('No method!')


@api_view(('DELETE','GET',))
def deleterepository(request):
    if request.method == 'DELETE':
        raw_dict = dict(zip(request.POST.keys(), request.POST.values()))
        raw_dict_key = list(raw_dict.keys())[0]
        repository_dict = ast.literal_eval(raw_dict_key)

        delete_id = repository_dict['delid']
        print(delete_id)

        if not delete_id:
            return Response('failed')
        else:
            get_object_or_404(Repository, pk=int(delete_id)).delete()
        return Response('success')

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


class DetailsearchViewset(viewsets.ModelViewSet):
    queryset = Detailsearch.objects.all()
    serializer_class = DetailsearchSerializer


class TempViewset(viewsets.ModelViewSet):
    queryset = Temp.objects.all()
    serializer_class = TempSerializer


class FolderViewset(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class CollectionViewset(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class RepositoryViewset(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class CorpusViewset(viewsets.ModelViewSet):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer





