# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from jidan.models import Quotes


# Mysql Pipeline
class MysqlPipeline(object):
    # 处理数据
    def process_item(self, item, spider):
        quotes = Quotes()
        quotes.text = item["text"]
        quotes.author = item["author"]
        quotes.tags = item["tags"]
        quotes.save()
