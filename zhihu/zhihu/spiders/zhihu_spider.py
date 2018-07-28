# -*- coding: utf-8 -*-
import json
import re
import scrapy


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['zhizhu.com']
    start_urls = ['https://www.zhihu.com']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def start_requests(self):
        '''登录页面'''
        post_url = "https://www.zhihu.com/#signin"
        yield scrapy.Request(
            url=self.start_urls,
            headers=self.headers,
            callback=self.login
        )

    def login(self, response):
        '''登录接口'''

        account = ""
        password = ""
        xsrf = ""

        content = response.content.decode("utf-8")
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', content)
        if match_obj:
            xsrf = (match_obj.group(1))

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"

            post_data = {
                "_xsrf": xsrf,
                "phone_num": account,
                "password": password,
            }

            yield scrapy.FormRequest(
                url=post_url,
                headers=self.headers,
                formdata=post_data,
                callback=self.parse
            )

        import time
        t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
        yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
                             callback=self.login_after_captcha)


    def login_after_captcha(self,response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha


        scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )

    def check_login(self,response):

        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.content.decode("utf-8"))
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)




    def parse(self, response):
        pass
