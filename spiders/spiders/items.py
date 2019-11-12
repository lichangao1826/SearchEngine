# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    hash_id = scrapy.Field()  # 全局唯一ID
    title = scrapy.Field()  # 标题
    link = scrapy.Field()  # 链接
    content = scrapy.Field()  # 内容
    publish_time = scrapy.Field()  # 发布时间
