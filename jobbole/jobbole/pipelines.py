# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import MySQLdb
import MySQLdb.cursors
from MySQLdb import connect
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi

from log_utils import logger
import codecs


class JobbolePipeline(object):
    def process_item(self, item, spider):
        logger.debug(item)
        return item


class MysqlPipeline(object):
    '''采用同步的机制方式'''

    def __init__(self):
        # 创建Connection连接
        self.conn = connect(host='localhost', port=3306, database='blogjobbole', user='root', password='mysql',
                            charset='utf8')
        #  #获得Cursor对象
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.insert_to_mysql(item)

    def insert_to_mysql(self, item):
        insert_sql = "insert into article(title, url, create_date, fav_nums) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    '''
        #使用twisted将mysql插入变成异步执行
    '''

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = "insert into article(title, url, create_date, fav_nums) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))


class ArticleImagePipeline(ImagesPipeline):
    '''
        获取保存到本地的图片路径
    '''

    def item_completed(self, results, item, info):
        if "front_image_url" in item:

            for ok, value_dict in results:
                image_file_path = value_dict.get("path")  # 获取保存的位置

            item["front_image_path"] = image_file_path

        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("blog.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_close(self, spider):
        self.file.close()


class JsonExporterPipleline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
