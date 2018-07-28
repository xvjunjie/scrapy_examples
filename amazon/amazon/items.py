# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class AmazonItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()



def strip_value(value):
    return value.strip()


class AmazonItem(scrapy.Item):

    Brand = scrapy.Field()#品牌
    review_num = scrapy.Field()
    score = scrapy.Field()#评分
    Primary_category= scrapy.Field(
        # output_processor=MapCompose(strip_value)
    )#一级类目
    Sales_volume= scrapy.Field()#销量
    Price =scrapy.Field()#售价
    ASIN = scrapy.Field()




