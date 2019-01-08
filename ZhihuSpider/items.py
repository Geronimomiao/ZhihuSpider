# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from ZhihuSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT

class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuQuestionItem(scrapy.Item):
    # 知乎问题 item
    zhihu_question_id = scrapy.Field()
    title = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    answer_nums = scrapy.Field()
    topics = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into zhihu_question (zhihu_question_id, title, answer_nums, topics, url) 
            values (%s, %s, %s ,%s, %s)
        '''

        zhihu_question_id = int(''.join(self["zhihu_question_id"]))
        answer_nums = self["answer_nums"][0]
        topics = ','.join(self["topics"])
        title = ''.join(self["title"])
        url = ''.join(self["url"])

        params = (zhihu_question_id, title, answer_nums, topics, url)
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎回答 item
    zhihu_answer_id = scrapy.Field()
    url = scrapy.Field()
    author_token = scrapy.Field()
    voteup_count = scrapy.Field()
    content = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    zhihu_question_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into zhihu_answer (zhihu_answer_id, url, author_token, voteup_count,
             content, zhihu_question_id, create_time, update_time, crawl_time) 
            values (%s, %s, %s ,%s, %s, %s, %s, %s, %s)
        '''
        # item_loader 传进来的字段 默认是 list
        # zhihu_answer_id = self["zhihu_answer_id"][0]
        topics = ','.join()
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (self["zhihu_answer_id"], self["url"], self["author_token"], self["voteup_count"], self["content"], self["zhihu_question_id"], self["create_time"], self["update_time"], self["crawl_time"])
        return insert_sql, params



