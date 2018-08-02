# -*- coding: utf-8 -*-

from openpyxl import Workbook


class AmazonPipeline(object):

    def open_spider(self, spider):
        self.work_book = Workbook()
        self.wa = self.work_book.active
        self.wa.append(['ASIN', '品牌', 'review数', '评分', '一级类目', '售价'])  # 设置表头

    def process_item(self, item, spider):
        print(item)

        line = [item['ASIN'], item['Brand'], item['review_num'], item['score'], item['Primary_category'],
                item['Price']]  # 把数据中每一项整理出来
        self.wa.append(line)  # 将数据以行的形式添加到xlsx中

        return item

    def close_spider(self, spider):
        self.work_book.save('baby_wash.xlsx')  # 保存xlsx文件
