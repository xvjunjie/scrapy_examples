# -*- coding: utf-8 -*-
import codecs

import scrapy
from douban.items import DoubanItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        li_list = response.xpath("//ol[@class='grid_view']/li")
        item = DoubanItem()
        for li in li_list:

            item['title_ch'] = response.xpath('//div[@class="hd"]//span[@class="title"][1]/text()').extract_first()
            # item["title_href"] = li.xpath(".//div[@class='hb']/a/@href").extract_first()
            item["rating_num"] = li.xpath(".//div[@class='star']/span[2]/text()").extract_first()
            item["image_urls"] = li.xpath(".//div[@class='pic']/a/img/@src").extract_first()
            item["topid"] = li.xpath(".//div[@class='pic']/em/text()").extract_first()

            # print(item)

            yield item

            # yield scrapy.Request(
            #     item["title_href"],
            #     callback=self.parse_detail,
            #     mate=item
            #
            # )

    def parse_detail(self):
        pass
