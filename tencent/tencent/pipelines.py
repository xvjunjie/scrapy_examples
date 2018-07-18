# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy import log, Item
from scrapy.exceptions import DropItem



class TencentPipeline(object):

    # def __init__(self):
    #     client = MongoClient(
    #         settings["MONGODB_SERVER"],
    #         settings["MONGODB_PORT"]
    #     )
    #     db = client[settings["MONGODB_DB"]]
    #     self.collection = db[settings["MONGODB_COLLECTION"]]

    def open_spider(self, spider):
        db_server = spider.settings.get("MONGODB_SERVER", "localhost")
        db_port = spider.settings.get("MONGODB_PORT", "27017")
        db_name = spider.settings.get("MONGODB_DB", "tencent_database")
        db_collection = spider.settings.get("MONGODB_COLLECTION", "hr_collection")

        self.db_client = MongoClient(db_server, db_port)
        self.db = self.db_client[db_name]
        self.db_collection = self.db[db_collection]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        '''
            插入数据
        :param item:
        :return:
        '''
        if isinstance(item, Item):
            item = dict(item)

            valid = True
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))
            if valid:
                # self.db.hr_collection.insert(item)
                self.db_collection.insert(item)
                # log.msg("Question added to MongoDB database!",
                #         level=log.DEBUG, spider=spider)
