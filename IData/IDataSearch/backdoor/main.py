import sys
import os
from scrapy.cmdline import execute


def execute_spider(name, word):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", name, '-a', 'keyword='+word])
