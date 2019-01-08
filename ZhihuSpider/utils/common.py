# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     common
   Description :    常用函数
   Author :       wsm
   date：          2019-01-08
-------------------------------------------------
   Change Activity:
                   2019-01-08:
-------------------------------------------------
"""
__author__ = 'wsm'

import re

def extract_num(text):
    # 从字符串 中 提取数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

