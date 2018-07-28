# -*- coding: utf-8 -*-

from openpyxl import Workbook


class AmazonPipeline(object):
    # Brand = scrapy.Field()  # 品牌
    # review_num = scrapy.Field()
    # score = scrapy.Field()  # 评分
    # Primary_category = scrapy.Field()  # 一级类目
    # Sales_volume = scrapy.Field()  # 销量
    # Price = scrapy.Field()  # 售价
    # ASIN = scrapy.Field()
    def __int__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['ASIN', '品牌', 'review数', '评分', '一级类目', '售价'])  # 设置表头

    def process_item(self, item, spider):
        line = [item['ASIN'], item['Brand'], item['review_num'], item['score'], item['Primary_category'],
                item['Price']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('/baby_wash.xlsx')  # 保存xlsx文件
        return item
