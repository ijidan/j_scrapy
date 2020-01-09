# -*- coding: utf-8 -*-
import scrapy


class ApiSpider(scrapy.Spider):
    name = 'api'
    allowed_domains = ['api.hianabian.com']
    start_urls = ['https://api.hianabian.com/']

    def parse(self, response):
        text = response.text
        text = text.encode("GB18030", "ignore")
        print response.text
