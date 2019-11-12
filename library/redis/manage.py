from redis import StrictRedis
from config.settings import REDIS_SERVER


class RedisManage(object):
    __client = None

    def __init__(self):
        self.__client = {}

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super(RedisManage, cls).__new__(cls)
        return cls._instance

    def execute(self, group='default'):
        if group not in self.__client:
            self.__client[group] = StrictRedis(**REDIS_SERVER[group], decode_responses=True)
        return self.__client[group]

    def __del__(self):
        if self.__client:
            del self.__client
