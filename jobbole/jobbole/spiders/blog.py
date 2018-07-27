# -*- coding: utf-8 -*-
import re

import datetime
import scrapy

from items import JobBoleArticleItem, ArticleItemLoader
from urllib import parse
from scrapy.loader import ItemLoader

from utils.common import get_md5


class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        div_list = response.xpath("//div[@class = 'grid-8']/div[1]")
        for div in div_list:
            '''
                处理文章详情页
            '''
            detail_url = div.xpath(".//div[@class='post-thumb']/a/@href").extract_first()
            front_image_url = div.xpath(".//div[@class='post-thumb']/a/img/@src").extract_first()  # 封面

            yield scrapy.Request(
                url=parse.urljoin(response.url, detail_url),
                callback=self.get_detail_use_item_loader,
                meta={"front_image_url": front_image_url}
            )

        '''
            处理下一页
            
        '''

        # next_url = item_loader.add_xpath("//a[@class ='next page-numbers']/@href").extract_first()
        # if next_url:
        #     yield scrapy.Request(
        #         url=parse.urljoin(item_loader.url, next_url),
        #         callback=parse
        #     )

    def get_detail_use_item_loader(self, response):
        '''
            使用item_loader,这里得到的字段是列表
        :return: 
        '''
        article_item = JobBoleArticleItem()
        item_loader = ArticleItemLoader(item=article_item, response=response)

        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))

        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader.add_value("front_image_url", [front_image_url])

        item_loader.add_xpath("title", "//div[@class = 'entry-header']/h1/text()")  # 标题
        item_loader.add_xpath("create_date", "//div[@class='entry-meta']/p/text()")
        item_loader.add_xpath("praise_nums", "//div[@class='post-adds']//h10/text()")# 点赞数
        item_loader.add_xpath("fav_nums", "//div[@class='post-adds']/span[2]/text()") # 收藏数
        item_loader.add_xpath("comment_nums",
                              "//span[@class='btn-bluet-bigger href-style hide-on-480']/text()")  # 评论数
        item_loader.add_xpath("content", "//div[@class='entry']") # 内容
        item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()") # 内容



        article_item = item_loader.load_item()

        yield article_item


'''

    def get_detail(self, item_loader):
            使用普通方式

        title = item_loader.add_xpath("//div[@class = 'entry-header']/h1/text()").extract_first()  # 标题
        create_date = item_loader.add_xpath("//div[@class='entry-meta']/p/text()").extract_first().strip().replace("·",
                                                                                                                "").strip()
    
        praise_nums = item_loader.add_xpath("//div[@class='post-adds']//h10/text()").extract_first()  # 点赞数
        fav_nums = item_loader.add_xpath("//div[@class='post-adds']/span[2]/text()").extract_first()  # 收藏数
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0
        comment_nums = item_loader.add_xpath(
            "//span[@class='btn-bluet-bigger href-style hide-on-480']/text()").extract_first()  # 评论数
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        else:
            comment_nums = 0
    
        content = item_loader.add_xpath("//div[@class='entry']").extract_first()  # 内容
        tag_list = item_loader.add_xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
    
        # 赋值
        article_item = JobBoleArticleItem()
        front_image_url = item_loader.meta.get("front_image_url", "")
        article_item["url_object_id"] = get_md5(item_loader.url)
        article_item["title"] = title
        article_item["url"] = item_loader.url
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]  # 注意这边
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content
    
        yield article_item
'''
