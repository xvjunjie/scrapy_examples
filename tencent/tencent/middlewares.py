# -*- coding: utf-8 -*-

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from tencent.user_agents import agents


class RotateUserAgentMiddleware(UserAgentMiddleware):
    # 从维护的UserAgent池中随机选取
    def process_request(self, request, spider):
        ua = random.choice(agents)
        if ua:
            print("********Current UserAgent:%s************" % ua)
            request.headers.setdefault('User-Agent', ua)


class CheckUserAgent:
    def process_response(self,request,response,spider):
        # print(dir(response.request))
        # print(request.headers["User-Agent"])
        return response