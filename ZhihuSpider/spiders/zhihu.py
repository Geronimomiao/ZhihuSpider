# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re
from scrapy.loader import ItemLoader
from ZhihuSpider.items import ZhihuAnswerItem, ZhihuQuestionItem

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
        ' capsion_ticket': '"2|1:0|10:1546675505|14:capsion_ticket|44:NGUyMzRjM2QxNTgwNDc1MDkxZDJlYzM4MWE2NjNhYWY=|325df9d74858fd80f4e350baccb860bd933961016cf40cd913dda359794d42bf"',
        '__gads': 'ID=b5560e541f6f5368:T=1546675490:S=ALNI_MbJUXfCnPkrdOZvVID8EaW07Fegrg',
        'l_n_c': '1',
        'n_c': '1',
        'l_cap_id': '"Mjk3M2Y4MGNlYzUzNGY1N2E2YzQ4ZjAwMWM2MGQ0M2I=|1546771518|8dbeef274759908ad5360fe64cd663f69d8ac434"',
        'r_cap_id': '"OWZjN2RlOTBjMDlmNGVlYjg0ZWU1OWMyYzk2NjM0MTA=|1546771518|4f50cae0e9c6f954960f4a9f8e8a67160ba92cc4"',
        'cap_id': '"NDRkYmFlMzVhOTZlNDdkMGFhZjhhZjJiZTY5MTM2ODI=|1546771518|c181720dd1f29b80daeb2157007192ec0078cf31"',

        ' __utmc':'155987696',
        ' __utmz':'155987696.1546771604.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        ' __utmv':'51854390.100--|2=registration_date=20180204=1^3=entry_date=20180204=1',
        ' __utma':'155987696.1161246750.1546771604.1546774463.1546777081.3',
        ' z_c0':'"2|1:0|10:1546846117|4:z_c0|92:Mi4xZGFPcEJ3QUFBQUFBQUNLWGZfWEdEaVlBQUFCZ0FsVk5wVTBnWFFDLTB6eDdGcnVsazBUSnAtdHNuQ1Y1UDNKcmFB|5c6982af3717b5389ec1cfd4b31173919f3f6aadec0ceb0a5994b1c0a5e4b5a7"',
        ' tgw_l7_route':'7bacb9af7224ed68945ce419f4dea76d',

        'capsion_ticket':'"2|1:0|10:1546846110|14:capsion_ticket|44:NWMxODA3NjhjZGZlNGNlNGE3ZWNlNGFlOTUwY2M5NWY=|a7867cec4fbc9c0fe3db93c48a20c5b50447fd373129c9f4e009ef68c5822846"'
    }
    headers = {
        "HOST": "www.zhihu.com",
        "referer": 'https://www.zhihu.com/signup?next=%2F',
        "User-Agent": agent,
    }

    def start_requests(self):
        # scrapy 框架 所以操作都是异步的
        # 如果不写 callback 默认调用 parse
        # callback 不能加括号 加括号 会调用给
        return [scrapy.Request('https://www.zhihu.com', headers=self.headers, cookies=self.cookies)]


    def parse(self, response):
        '''
        scrapy 框架是基于 深度优先 算法实现的
        提取出 页面 所有 url 并跟踪这些 url 进一步爬去
        如果 提取的 url 格式 为 /question/xxx 就进行 进一步的提取
        '''
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # all_urls = filter(lambda x:True if x.startswith('https') else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                # scrapy 通过 yield 将 url 提交给下载器
                # dont_filter=True 停用过滤功能 否则无法发起请求
                # 默认只能请求此处的 allowed_domains = ['https://www.zhihu.com']
                yield scrapy.Request(request_url, headers=self.headers, meta={"question_id": question_id}, callback=self.parse_question, dont_filter=True)
            # else:
                #如果不是question页面则直接进一步跟踪
                # yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        # 处理 question 页面 从页面中提取具体的 question item
        title = response.css("h1").extract()
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', '.QuestionHeader-title::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('zhihu_question_id', response.meta.get('question_id', 0))
        item_loader.add_css('answer_nums', 'a.QuestionMainAction::text')
        item_loader.add_css('topics', '.QuestionHeader-tags .Popover::text')

        question_item = item_loader.load_item()
        pass


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