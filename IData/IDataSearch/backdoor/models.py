from datetime import datetime
from django.utils import timezone
from django.db import models
from rest_framework import serializers
# Create your models here.


class Message(models.Model):
	subject = models.TextField(max_length=3)
	body = models.TextField(max_length=200)


class MessageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Message
		fields = ('url', 'subject', 'body', 'pk')


class Extractor(models.Model):
	originkws = models.CharField(max_length=200)


class ExtractorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Extractor
		fields = ('url', 'originkws', 'pk')


class Recommend(models.Model):
	recommendkws = models.CharField(max_length=200)


class RecommendSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Recommend
		fields = ('url', 'recommendkws', 'pk')


class Simplesearch(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=50)
	source = models.CharField(max_length=10)
	info = models.TextField()
	date = models.TextField()
	kws = models.CharField(max_length=50)
	cited = models.TextField()
	downed = models.TextField()
	download = models.TextField()
	abstract = models.TextField()
	fund = models.TextField()


class SimplesearchSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Simplesearch
		fields = ('url', 'title', 'author', 'source', 'info', 'date', 'kws', 'cited', 'downed', 'download', 'abstract', 'fund', 'pk')



'''
# connect scrapy spiders

class Idata(models.Model):
	d_url = models.URLField()
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=50)
	source = models.CharField(max_length=10)
	info = models.TextField()
	date = models.TextField()
	kws = models.CharField(max_length=50)
	cited = models.PositiveIntegerField()
	downed = models.PositiveIntegerField()
	download = models.URLField()
	abstract = models.TextField()
	fund = models.TextField()

	class Meta:
		verbose_name = 'idataspider'

'''