# -*- coding:utf-8 -*-
from scrapy import cmdline
import os, sys
from tencent.tencent.log_utils import logger

logger.debug(sys.path)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
cmdline.execute(["scrapy", "crawl", "tencent_hr"])
