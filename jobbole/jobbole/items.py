# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


# class JobboleItem(scrapy.Item):
#     '''
#         正常定义字段
#     '''
#     title = scrapy.Field()
#     create_date = scrapy.Field()
#     url = scrapy.Field()
#     url_object_id = scrapy.Field()
#     front_image_url = scrapy.Field()
#     front_image_path = scrapy.Field()
#     praise_nums = scrapy.Field()
#     comment_nums = scrapy.Field()
#     fav_nums = scrapy.Field()
#     tags = scrapy.Field()
#     content = scrapy.Field()


def add_jobbole(value):
    # values 表示title传进来的值
    return value + "jobbole"


def date_convert(value):
    '''时间转换'''
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def re_fav_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        fav_nums = match_re.group(1)
    else:
        fav_nums = 0
    return fav_nums




class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()




class JobBoleArticleItem(scrapy.Item):
    '''
        item_loader
    '''
    title = scrapy.Field(
        # 表示数据传递进来的时候，可以做些预处理
        input_processor=MapCompose(add_jobbole)
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()  # 取一个；没有这句，取的是列表
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
