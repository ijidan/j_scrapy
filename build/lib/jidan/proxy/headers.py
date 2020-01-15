# -*- coding: utf-8 -*-

from fake_useragent import UserAgent


# 获取随机 user agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# 随机header
def get_request_headers(referer='https://www.baidu.com'):
    random_user_agent = get_random_user_agent()
    headers = {
        'User-Agent': random_user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': referer,
        'Accept-Encoding': 'gzip, deflate,br',
        'Connection': 'keep-alive',
    }
    return headers
