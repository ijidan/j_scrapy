# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['https://httpbin.org/get?show_env=1']

    def parse(self, response):
        text = response.text
        text = text.encode("GB18030", "ignore")
        print(response.text)


if __name__ == "__main__":
    cmdline.execute("scrapy crawl httpbin".split())
