# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import logging
from jidan.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = BeautifulSoup(response.text, 'lxml')
        for quote in quotes.find_all(name='div', class_='quote'):
            item = QuotesItem()  # 使用items中定义的数据结构
            for s in quote.find_all(name='span', class_='text'):
                item['text'] = s.text
            for s in quote.find_all(name='small', class_='author'):
                item['author'] = s.text
            for s in quote.find_all(name='div', class_='tags'):
                item['tags'] = s.text.replace('\n', '').strip().replace(' ', '')
            yield item

        nexts = quotes.find_all(name='li', class_='next')
        for next in nexts:
            n = next.find(name='a')
            url = 'http://quotes.toscrape.com/' + n['href']
            yield scrapy.Request(url=url, callback=self.parse)
