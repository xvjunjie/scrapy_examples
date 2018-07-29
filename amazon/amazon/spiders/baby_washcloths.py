# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from items import AmazonItemLoader, AmazonItem


class BabyWashclothsSpider(scrapy.Spider):
    name = 'baby_washcloths'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbaby-products&field-keywords=baby+washcloths&rh=n%3A165796011%2Ck%3Ababy+washcloths']

    headers = {
        "HOST": "www.amazon.com",
        "Referer": "https://www.amazon.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        li_list = response.xpath("//div[@id='atfResults']/ul/li")
        for li in li_list:
            detail_url = li.xpath(".//div[@class='a-row a-spacing-none a-spacing-top-mini']/a/@href").extract_first()

            yield scrapy.Request(
                url=parse.urljoin(response.url, detail_url),
                headers=self.headers,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        # Brand = scrapy.Field()  # 品牌
        # review_num = scrapy.Field()
        # score = scrapy.Field()  # 评分
        # Primary_category = scrapy.Field()  # 一级类目
        # Sales_volume = scrapy.Field()  # 销量
        # Price = scrapy.Field()  # 售价
        # ASIN = scrapy.Field()

        amazon_item = AmazonItem()
        amazon_loader = AmazonItemLoader(item=amazon_item, response=response)

        amazon_loader.add_xpath("Brand", "//a[@id='bylineInfo']/text()")
        amazon_loader.add_xpath("review_num", "//span[@id='acrCustomerReviewText']/text()")
        amazon_loader.add_xpath("score", "//div[@id='averageCustomerReviews']//span[@class='a-icon-alt']/text()")

        amazon_loader.add_xpath("ASIN", "//div[@class='pdTab//']//tr[1]//td[@class='value']/text()")
        amazon_loader.add_xpath("Price", "//span[@id='priceblock_ourprice']/text()")
        amazon_loader.add_xpath("Primary_category", "//div[@class='pdTab//']//tr[@id='SalesRank']/td[@class='value']/text()")

        amazon_item = amazon_loader.load_item()

        yield amazon_item
