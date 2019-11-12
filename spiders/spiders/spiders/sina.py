# -*- coding: utf-8 -*-
from ..items import NewsItem
import requests
import hashlib
import scrapy
import random
import json
import time


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']

    BASE_URL = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}&r={}'
    PAGE_SIZE = 50

    def start_requests(self):
        page_count = self._get_total_page() // self.PAGE_SIZE
        for page in range(1, page_count + 1):
            rand = random.random()
            yield scrapy.Request(
                url=self.BASE_URL.format(page, rand),
                callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        for news in data['result']['data']:
            yield scrapy.Request(
                url=news.get('url'),
                meta={"news": news},
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        item = NewsItem()
        news = response.meta.get('news')
        item['title'] = news.get('title')
        item['link'] = news.get('url')
        item['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(news.get('ctime'))))
        content_xpath = response.xpath('//*[@id="artibody"]/p/text()') or response.xpath('//*[@id="article"]/p/text()')
        item['content'] = ''.join([_.strip() for _ in content_xpath.extract()])
        item['hash_id'] = self._calc_text_hash(item['content'])
        yield item

    @classmethod
    def _calc_text_hash(cls, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @classmethod
    def _get_total_page(cls):
        rand = random.random()
        result = requests.get(cls.BASE_URL.format(1, rand))
        res = json.loads(result.text)
        total_num = res['result']['total']

        return total_num
