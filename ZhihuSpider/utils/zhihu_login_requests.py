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
# 伪造请求头 有些网站会对 header 做要求
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

header = {
    "HOST": "www.zhihu.com",
    "Referer": 'https://www.zhihu.com',
    "User-Agent": agent,
    'Content-Type': 'application/json',
    'cookie': 'tgw_l7_route=116a747939468d99065d12a386ab1c5f; _zap=36aae2c1-1d0a-4411-9955-1a3f43098840; _xsrf=bXrbf8r0ti5ffzGUsQhv9JlQw3ZuFJeT; d_c0="AAAil3_1xg6PTm3cJjSz3vITatQ4DbGdN_g=|1546650079"; capsion_ticket="2|1:0|10:1546650093|14:capsion_ticket|44:NTBmNmQ4ZTRlZTJmNDY4MThmZmQ3NzViMjhjN2Q0YjQ=|2990647369021636cc9acf941607df8b197a5ddd65c826b87d7752c6b776c4ee"; z_c0="2|1:0|10:1546650111|4:z_c0|92:Mi4xZGFPcEJ3QUFBQUFBZ0NOcWZfWEdEaVlBQUFCZ0FsVk5fMDhkWFFBZG1hUkZxZ3ZTZUlpdExTUG52OWk5Z0hYbUlR|7b8c31255abd1fa640d09dfc1828c05cc73d31ec8d87c919e19edf04c5497eb0"; tst=r; q_c1=858fd43565ab4568a3e0a4a1c563937f|1546650114000|1546650114000'
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

# get_index()
is_login()