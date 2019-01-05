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


from scrapy.cmdline import execute

execute(["scrapy", "crawl", "zhihu"])