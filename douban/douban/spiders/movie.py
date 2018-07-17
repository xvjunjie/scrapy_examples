# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


# title_ch = scrapy.Field()  # 中文标题
# # title_en = scrapy.Field()   # 外文名字
# # title_ht = scrapy.Field()   # 港台名字
# # detail = scrapy.Field()     # 导演主演等信息
# rating_num = scrapy.Field()  # 分值
# rating_count = scrapy.Field()  # 评论人数
# # quote = scrapy.Field()      # 短评
# image_urls = scrapy.Field()  # 封面图片地址
# topid = scrapy.Field()  # 排名序号

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        li_list = response.xpath("//ol[@class='grid_view']/li")
        for li in li_list:
            item = DoubanItem()
            item['title_ch'] = response.xpath('//div[@class="hd"]//span[@class="title"][1]/text()').extract()            # item["title_href"] = li.xpath(".//div[@class='hb']/a/@href").extract_first()
            item["rating_num"] = li.xpath(".//div[@class='star']/span[2]/text()").extract_first()
            item["image_urls"] = li.xpath(".//div[@class='pic']/a/img/@src").extract_first()
            item["topid"] = li.xpath(".//div[@class='pic']/em/text()").extract_first()

            print(item)

            yield item

            # yield scrapy.Request(
            #     item["title_href"],
            #     callback=self.parse_detail,
            #     mate=item
            #
            # )

    def parse_detail(self):
        pass
