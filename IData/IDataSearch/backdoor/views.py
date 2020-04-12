import json
from .utils import ExtractAndRecommend


from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.forms.models import model_to_dict
from .models import Message, Extractor, Recommend, MessageSerializer, ExtractorSerializer, RecommendSerializer


@api_view(('GET',))
def extract(request):
    serializer_context = {
        'request': request,
    }

    latest = Message.objects.last()
    raw_dict = model_to_dict(latest)
    ex = ExtractAndRecommend()
    extr_kws = ex.extract_kws(raw_dict)
    for kws in extr_kws:
        extr = Extractor(originkws=kws)
        extr.save()

        # retrieve kws
        data = Extractor.objects.filter(originkws=kws)
        for d in data:
            d_dict = model_to_dict(d)
            pkid = d_dict['id']

            extractor = ExtractorSerializer(data=d_dict, context=serializer_context)
            if extractor.is_valid():
                ordered_li = extractor.validated_data
                ordered_li['pk'] = pkid
                print(ordered_li)
                return Response(ordered_li)


@api_view(('GET',))
def recommend(request):
    serializer_context = {
        'request': request,
    }

    latest = Message.objects.last()
    raw_dict = model_to_dict(latest)
    ex = ExtractAndRecommend()
    recom_kws = ex.recommend_kws(raw_dict)
    for rkws in recom_kws:
        recom = Recommend(recommendkws=rkws)
        recom.save()

        # retrieve kws
        data = Recommend.objects.filter(recommendkws=rkws)
        for d in data:
            d_dict = model_to_dict(d)
            pkid = d_dict['id']

            recommend = RecommendSerializer(data=d_dict, context=serializer_context)
            if recommend.is_valid():
                ordered_li = recommend.validated_data
                ordered_li['pk'] = pkid
                print(ordered_li)
                return Response(ordered_li)


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
















