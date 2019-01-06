# -*- coding: utf-8 -*-
import scrapy

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['https://www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    cookies = 'tgw_l7_route=116a747939468d99065d12a386ab1c5f; _zap=36aae2c1-1d0a-4411-9955-1a3f43098840; _xsrf=bXrbf8r0ti5ffzGUsQhv9JlQw3ZuFJeT; d_c0="AAAil3_1xg6PTm3cJjSz3vITatQ4DbGdN_g=|1546650079"; capsion_ticket="2|1:0|10:1546650093|14:capsion_ticket|44:NTBmNmQ4ZTRlZTJmNDY4MThmZmQ3NzViMjhjN2Q0YjQ=|2990647369021636cc9acf941607df8b197a5ddd65c826b87d7752c6b776c4ee"; z_c0="2|1:0|10:1546650111|4:z_c0|92:Mi4xZGFPcEJ3QUFBQUFBZ0NOcWZfWEdEaVlBQUFCZ0FsVk5fMDhkWFFBZG1hUkZxZ3ZTZUlpdExTUG52OWk5Z0hYbUlR|7b8c31255abd1fa640d09dfc1828c05cc73d31ec8d87c919e19edf04c5497eb0"; tst=r; q_c1=858fd43565ab4568a3e0a4a1c563937f|1546650114000|1546650114000'
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": 'https://www.zhihu.com',
        "User-Agent": agent,
        'Content-Type': 'application/json',
        'cookie': cookies
    }


    def parse(self, response):
        pass


    def start_requests(self):
        # scrapy 框架 所以操作都是异步的
        # 如果不写 callback 默认调用 parse
        # callback 不能加括号 加括号 会调用给
        return [scrapy.Request('https://www.zhihu.com', headers=self.headers,callback=self.login)]


    def login(self, response):
        res = response.text
        return [scrapy.FormRequest(
            url='https://www.zhihu.com/login/phone_num',
            formdata={
                "_xsrf": '',
                "phone_num": '13088888888',
                "password": '123456',
            },
            headers=self.headers,
            callback=self.checkLogin
        )]

    def checkLogin(self):
        # 通过个人中心页面 返回状态码 来判断是否为登录状态
        pass