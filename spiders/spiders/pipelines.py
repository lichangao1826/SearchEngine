# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo.errors import DuplicateKeyError


class SpidersPipeline(object):
    def process_item(self, item, spider):
        return item


class SpidersMongoPipeline(object):
    COLLECTION_NAME = 'documents'

    _db = None
    _client = None
    _collection = None

    def __init__(self, mongo_uri, mongo_db):
        self._mongo_uri = mongo_uri
        self._mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        self._client = pymongo.MongoClient(self._mongo_uri)
        self._db = self._client[self._mongo_db]
        self._collection = self._db[self.COLLECTION_NAME]

    def close_spider(self, spider):
        self._client.close()

    def process_item(self, item, spider):
        try:
            self._collection.insert_one(dict(item))
            return item
        except DuplicateKeyError:
            spider.logger.debug("duplicate key error collection")
            return item
