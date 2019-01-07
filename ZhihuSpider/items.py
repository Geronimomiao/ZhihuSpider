# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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




