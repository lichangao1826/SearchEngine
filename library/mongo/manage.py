from config.settings import MONGO_SERVER
import pymongo


class MongoManage(object):
    __client = None

    def __init__(self):
        self.__client = {}

    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            cls._instance = super(MongoManage, cls).__new__(cls)
        return cls._instance

    def execute(self, database, table, group="default"):
        if group not in self.__client:
            self.__client[group] = pymongo.MongoClient(**MONGO_SERVER[group])
        return self.__client[group][database][table]

    def __del__(self):
        if self.__client:
            del self.__client
