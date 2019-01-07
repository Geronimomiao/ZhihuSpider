# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       wsm
   date：          2019-01-04
-------------------------------------------------
   Change Activity:
                   2019-01-04:
-------------------------------------------------
"""
__author__ = 'wsm'

# 知乎 api 接口
# https://www.zhihu.com/api/v4/members/yangtong-78?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge%5B?(type=best_answerer)%5D.topics
# https://www.zhihu.com/api/v4/questions/284206141/answers?include=content,data[*].voteup_count&limit=200&offset=30&sort_by=default

from scrapy.cmdline import execute

execute(["scrapy", "crawl", "zhihu"])


