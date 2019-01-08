# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re, json, datetime
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
        '_xsrf':'bXrbf8r0ti5ffzGUsQhv9JlQw3ZuFJeT',
        'd_c0':'"AAAil3_1xg6PTm3cJjSz3vITatQ4DbGdN_g=|1546650079"',
        'tst':'r',
        'q_c1':'858fd43565ab4568a3e0a4a1c563937f|1546650114000|1546650114000',
        '__gads':'ID=b5560e541f6f5368:T=1546675490:S=ALNI_MbJUXfCnPkrdOZvVID8EaW07Fegrg',
        'l_n_c':'1',
        'n_c':'1',
        '__utmc':'51854390',
        '__utmv':'51854390.100--|2=registration_date=20180204=1^3=entry_date=20180204=1',
        'cap_id':'"YzFjNWFhMDlhMTFlNDcxMTlhNmEyNDY2NTQ0Mjg0NjU=|1546920964|bef37a7b5403d16843c24eb4a41e6db0c29fc209"',
        'r_cap_id':'"ZTI4YTA5MDBlNmQ0NGU3Yjg4ZTAxZTQ3NTNkZTllODI=|1546920964|d2f587704cf7029e83648606b179db1a0b340ca4"',
        'l_cap_id':'"NzU3MmJkOTVhYzUyNGYwNWJkMWQzMWUwZDFiZTUyNGE=|1546920964|9ddb7fafe39f49c7a3490eef038b4b7fa0f698bf"',
        'capsion_ticket':'"2|1:0|10:1546920967|14:capsion_ticket|44:OTI3NzY3YWFhMDY1NDM5Yzg5MTNhOWU1MWFmNmZiZTA=|4b347a44f2b648b28a6fbad265a362c3cb780523a7fe264f761c95380b4fd0d3"',
        'z_c0':'"2|1:0|10:1546920974|4:z_c0|92:Mi4xZGFPcEJ3QUFBQUFBQUNLWGZfWEdEaVlBQUFCZ0FsVk5EbkloWFFCcWp4cFFncTFGVUFxYmhockphbU1vNWEzbkx3|1d4ac2584159adc51d1f5936c0a43ea5483f335897cd2fe301aa679d97aa0d39"',
        'tgw_l7_route':'f2979fdd289e2265b2f12e4f4a478330',
        '__utma':'51854390.1862793109.1546908601.1546908601.1546933166.2',
        '__utmb':'51854390.0.10.1546933166',
        '__utmz':'51854390.1546933166.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',

    }
    headers = {
        "HOST": "www.zhihu.com",
        "referer": 'https://www.zhihu.com/signup?next=%2F',
        "User-Agent": agent,
    }
    # question 的 第一页 answer 起始 url
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=content,data[*].voteup_count&limit={1}&offset={2}&sort_by=default'

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
            #     # 如果不是question页面则直接进一步跟踪
            #     # yield scrapy.Request(url, headers=self.headers, callback=self.parse, dont_filter=True, cookies=self.cookies)
            #     yield scrapy.Request(url, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse_question(self, response):
        # 处理 question 页面 从页面中提取具体的 question item
        # title = response.css(".QuestionHeader-title::text").extract()
        # answer_nums = response.css(".List-headerText span::text").extract()
        # topics = response.css('.QuestionHeader-topics .Popover div::text').extract()
        question_id = response.meta.get('question_id', 0)
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', '.QuestionHeader-title::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('zhihu_question_id', question_id)
        item_loader.add_css('answer_nums', '.List-headerText span::text')
        item_loader.add_css('topics', '.QuestionHeader-topics .Popover div::text')

        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer, dont_filter=True)
        yield question_item


    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]
        # 提取 answer 的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_answer_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['author_token'] = answer['author']['url_token']
            answer_item['voteup_count'] = answer['voteup_count']
            answer_item['content'] = answer['content']
            answer_item['zhihu_question_id'] = answer['question']['id']
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['updated_time']
            answer_item['crawl_time'] = datetime.datetime.now()

            yield answer_item


        # 继续扒 后面的回答
        # if not is_end:
        #     yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer, dont_filter=True)

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