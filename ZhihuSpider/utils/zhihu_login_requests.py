# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     zhihu_login_requests
   Description :   知乎的模拟登录
   Author :       wsm
   date：          2019-01-04
-------------------------------------------------
   Change Activity:
                   2019-01-04:
-------------------------------------------------
"""
__author__ = 'wsm'

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie 未能加载")

# 现接口已失效
# 通过在请求头 设置 cookie 模拟登录
# 伪造请求头 有些网站会对 header 做要求
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

header = {
    "HOST": "www.zhihu.com",
    "Referer": 'https://www.zhihu.com',
    "User-Agent": agent,
    'Content-Type': 'application/json',
    'cookie': '_zap=36aae2c1-1d0a-4411-9955-1a3f43098840; _xsrf=bXrbf8r0ti5ffzGUsQhv9JlQw3ZuFJeT; d_c0="AAAil3_1xg6PTm3cJjSz3vITatQ4DbGdN_g=|1546650079"; tst=r; q_c1=858fd43565ab4568a3e0a4a1c563937f|1546650114000|1546650114000; __utmc=51854390; __utmz=51854390.1546653917.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/miao-75-45-93/activities; __utmv=51854390.100--|2=registration_date=20180204=1^3=entry_date=20180204=1; __utma=51854390.1656210164.1546653917.1546653917.1546655910.2; __gads=ID=b5560e541f6f5368:T=1546675490:S=ALNI_MbJUXfCnPkrdOZvVID8EaW07Fegrg; capsion_ticket="2|1:0|10:1546675505|14:capsion_ticket|44:NGUyMzRjM2QxNTgwNDc1MDkxZDJlYzM4MWE2NjNhYWY=|325df9d74858fd80f4e350baccb860bd933961016cf40cd913dda359794d42bf"; z_c0="2|1:0|10:1546675511|4:z_c0|92:Mi4xZGFPcEJ3QUFBQUFBQUNLWGZfWEdEaVlBQUFCZ0FsVk5ON01kWFFCVXUxOTkwX21oOVdVdl82OUQ1b2E0R1BMdkNR|880196b4d027ac5f4efad1cd6827b936aa5f9ac74806fb788862c0920a1f2fb5"; tgw_l7_route=a37704a413efa26cf3f23813004f1a3b'
}

def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    print(response.text)
    return ''

def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print('手机号登录')
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            "_xsrf": get_xsrf,
            "phone_num": account,
            "password": password
        }

        response_text = session.post(post_url, data=post_data, headers=header)
        # 将服务器 返回的 cookies 保存到本地
        session.cookies.save()


def is_login():
    # 通过查看个人中心 的返回码状态 判断是否登录
    inbox_url = 'https://www.zhihu.com/inbox'
    # allow_redirects=False 否则会跳转至登录页面
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True
    pass

def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open('index_page.html', 'wb') as f:
        f.write(response.text.encode('utf-8'))
    print('ok')

get_index()
# is_login()