# -*- coding: utf-8 -*-
import scrapy

'''
由于知乎 登录加密 方式 过于复杂
此处 采用 此处采用手动 写入 cookies 的方法
来对网站 进行爬去
'''
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['https://www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    cookies = {
        '_zap':'36aae2c1-1d0a-4411-9955-1a3f43098840',
        ' _xsrf':'bXrbf8r0ti5ffzGUsQhv9JlQw3ZuFJeT',
        ' d_c0':'"AAAil3_1xg6PTm3cJjSz3vITatQ4DbGdN_g=|1546650079"',
        ' tst':'r',
        ' q_c1':'858fd43565ab4568a3e0a4a1c563937f|1546650114000|1546650114000',
        ' __utmc':'51854390',
        ' __utmz':'51854390.1546653917.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/miao-75-45-93/activities',
        ' __utmv':'51854390.100--|2=registration_date=20180204=1^3=entry_date=20180204=1',
        ' __utma':'51854390.1656210164.1546653917.1546653917.1546655910.2',
        ' __gads':'ID=b5560e541f6f5368:T=1546675490:S=ALNI_MbJUXfCnPkrdOZvVID8EaW07Fegrg',
        ' capsion_ticket':'"2|1:0|10:1546675505|14:capsion_ticket|44:NGUyMzRjM2QxNTgwNDc1MDkxZDJlYzM4MWE2NjNhYWY=|325df9d74858fd80f4e350baccb860bd933961016cf40cd913dda359794d42bf"',
        ' z_c0':'"2|1:0|10:1546675511|4:z_c0|92:Mi4xZGFPcEJ3QUFBQUFBQUNLWGZfWEdEaVlBQUFCZ0FsVk5ON01kWFFCVXUxOTkwX21oOVdVdl82OUQ1b2E0R1BMdkNR|880196b4d027ac5f4efad1cd6827b936aa5f9ac74806fb788862c0920a1f2fb5"',
        ' tgw_l7_route':'a37704a413efa26cf3f23813004f1a3b'
    }
    headers = {
        "HOST": "www.zhihu.com",
        "referer": 'https://www.zhihu.com/signup?next=%2F',
        "User-Agent": agent,
    }


    def parse(self, response):
        pass


    def start_requests(self):
        # scrapy 框架 所以操作都是异步的
        # 如果不写 callback 默认调用 parse
        # callback 不能加括号 加括号 会调用给
        return [scrapy.Request('https://www.zhihu.com', headers=self.headers, cookies=self.cookies)]


    # def login(self, response):
    #     res = response.text
    #     return [scrapy.FormRequest(
    #         url='https://www.zhihu.com/login/phone_num',
    #         formdata={
    #             "_xsrf": '',
    #             "phone_num": '13088888888',
    #             "password": '123456',
    #         },
    #         callback=self.checkLogin
    #     )]
    #
    # def checkLogin(self):
    #     # 通过个人中心页面 返回状态码 来判断是否为登录状态
    #     pass