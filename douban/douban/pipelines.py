# -*- coding: utf-8 -*-
from pymongo import MongoClient

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class DoubanPipeline(object):

    client = MongoClient()
    db = client["python_database"]
    douban_table = db["douban_collection "]



    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid=False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            self.douban_table.insert(dict(item))

        return item

