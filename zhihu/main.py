# -*- coding:utf-8 -*-
from scrapy import cmdline
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
cmdline.execute(["scrapy", "crawl", "zhihu_spider"])
