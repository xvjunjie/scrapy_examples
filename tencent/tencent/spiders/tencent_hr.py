# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencentHrSpider(scrapy.Spider):
    name = 'tencent_hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        item = TencentItem()
        for tr in tr_list:

            item["title"] = tr.xpath("./td[1]/a/text()").extract_first()
            item["position"] = tr.xpath("./td[2]/text()").extract_first()
            item["publish_date"] = tr.xpath("./td[5]/text()").extract_first()

            print(item)

            yield item
