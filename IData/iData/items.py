# -*- coding: utf-8 -*-

# Define here the models for your scraped selfs
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/selfs.html

import scrapy
from scrapy_djangoitem import DjangoItem
from backdoor.models import Idata


class IdataItem(DjangoItem):
    django_model = Idata




