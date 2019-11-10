# -*- coding: utf-8 -*-
from ..items import NewsItem
import scrapy
import time
import json


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['is.snssdk.com']

    headers = {
        'Accept': 'image/webp,image/*;q=0.8',
        'User-Agent': 'News/6.9.8.36 CFNetwork/975.0.3 Darwin/18.2.0',
        'Accept-Language': 'zh-cn'
    }

    channels = ['news_tech']

    BASE_URL = 'http://is.snssdk.com/api/news/feed/v51/'

    def start_requests(self):
        for i, channel in enumerate(self.channels):
            yield scrapy.Request(
                self.BASE_URL,
                body=self._generate_params(channel),
                meta={'cookiejar': i},
                callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        for i in range(data['total_number']):
            info = json.loads(data['data'][i]['content'])
            item = NewsItem()
            item['title'] = info.get('title', '')
            item['link'] = info.get('article_url', '')
            item['abstract'] = info.get('abstract', '')
            item['content'] = ''  # TODO
            item['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info['publish_time']))
            yield item

    @classmethod
    def _generate_params(cls, channel):
        current_time = int(time.time())
        last_request_time = current_time - 500
        params = {
            # 频道名
            'category': channel,
            # 固定值 1 ？
            'refer': '1',
            # 返回数量，默认为 20
            'count': '20',
            # 上次请求时间的时间戳，例：1491981025
            'min_behot_time': last_request_time,
            # 本次请求时间的时间戳，例：1491981165
            'last_refresh_sub_entrance_interval': current_time - 10,
            # 本地时间
            'loc_time': int(current_time / 1000) * 1000,
            # 经度
            'latitude': '',
            # 纬度
            'longitude': '',
            # 当前城市
            'city': '',
            # 某个唯一 id，长度为 10
            'iid': '1234876543',
            # 设备 id，长度为 11
            'device_id': '42433242851',
            'abflag': '3',
            'ssmix': 'a',
            'language': 'zh',
            # 某个唯一 id，长度为 16
            'openudid': '1b8d5bf69dc4a561',
        }

        return json.dumps(params)
