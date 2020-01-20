# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
from scrapy import signals
import os
from jidan.utils import Logger
from jidan.proxy.xici import XiCi


class JidanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JidanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 随机User-Agent,随机算法需要更改
class RandomUserAgentMiddleware(object):

    def __init__(self, crawler):
        location = os.getcwd() + '/jidan/fake_useragent.json'
        print("==========="+location+"===================")
        if os.path.exists(location):
            self.ua = UserAgent(path=location)
        else:
            self.ua = UserAgent(use_cache_server=False, cache=False, verify_ssl=False)
        self.logger = Logger()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler)
        return s

    def process_request(self, request, spider):
        current_ua = self.ua.random
        self.logger.error(current_ua)
        request.headers["User-Agent"] = current_ua


class ProxyMiddleware(object):
    def __init__(self, crawler):
        self.logger = Logger()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler)
        return s

    def process_request(self, request, spider):
        xici = XiCi()
        proxy = xici.get_one_valid_proxy()
        if proxy is not None:
            self.logger.error("proxy:" + proxy + "=====================")
            request.meta['proxy'] = proxy
        return None
