# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from items import AmazonItem, AmazonItemLoader


class ShopInfoSpider(scrapy.Spider):
    name = 'shop_info'

    check_website = "www.amazon.com"
    key_word = "baby washcloths"  # 关键字

    allowed_domains = [check_website]
    start_urls = ["https://%s/s/ref=nb_sb_noss?url=search-alias&field-keywords=%s" % (
    check_website, key_word.replace(" ", "+"))]  # 搜索页url
    check_pro_asin = "B074QRB1KB"  # 查找产品asin码

    # https: // www.amazon.com / s / ref = nb_sb_noss?url = search - alias & field - keywords = baby + washcloths & rh = n % 3A165796011 % 2Ck % Ababy + washcloths % 27
    # start_urls = ['http://amazon.com/']
    headers = {
        "HOST": "www.amazon.com",
        "Referer": "https://www.amazon.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }


    def start_requests(self):
        for url in self.start_urls:
            return [
                scrapy.Request(url, headers=self.headers, callback=self.parse_pro_url, dont_filter=True)]  # 搜索第一页开始爬取

    def parse_pro_url(self, response):
        li_list = response.xpath("//*[@id='s-results-list-atf']/li")
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
        # Primary_category = scrapy.Field(
        #     input_processor=MapCompose(strip_value),
        # )  # 一级类目
        # Sales_volume = scrapy.Field()  # 销量
        # Price = scrapy.Field()  # 售价
        # ASIN = scrapy.Field(
        #     input_processor=MapCompose(asin_value),
        # )

        amazon_item = AmazonItem()
        amazon_loader = AmazonItemLoader(item=amazon_item, response=response)

        amazon_loader.add_xpath("Brand", "//a[@id='bylineInfo']/text()", "没有品牌")
        amazon_loader.add_xpath("review_num", "//span[@id='acrCustomerReviewText']/text()", 0)
        amazon_loader.add_xpath("score", "//div[@id='averageCustomerReviews']//span[@class='a-icon-alt']/text()","没有评分")
        amazon_loader.add_xpath("Price", "//span[@id='priceblock_ourprice']/text()")
        amazon_loader.add_xpath("ASIN",
                                "//*[@id='prodDetails']/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]/text()","ASIN")
        amazon_loader.add_xpath("Primary_category", "//*[@id='SalesRank']/td[2]/text()", "没有分类")
        amazon_item = amazon_loader.load_item()

        yield amazon_item
