from django.db import models

# Create your models here.


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

