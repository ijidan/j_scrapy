# -*- coding: utf-8 -*-

import scrapy

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        text = response.text
        text = text.encode("GB18030", "ignore")
        print(text)
