# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy import log
from scrapy.exceptions import DropItem

from tencent import settings


class TencentPipeline(object):

    def __init__(self):
        client = MongoClient(
            settings["MONGODB_SERVER"],
            settings["MONGODB_PORT"]
        )
        db = client[settings["MONGODB_DB"]]
        self.collection = db[settings["MONGODB_COLLECTION"]]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            # log.msg("Question added to MongoDB database!",
            #         level=log.DEBUG, spider=spider)
        return item



