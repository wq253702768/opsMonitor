#!/usr/bin/env python
# coding: utf-8
import redis
from django.conf import settings


class RedisApi(object):
    def __init__(self):
        self.host = settings.REDIS_URL
        self.port = settings.REDIS_PORT
        self.db = settings.REDIS_DB
        self.rc = self.conn_redis()

    def conn_redis(self):
        rc =redis.StrictRedis(host=self.host, port=self.port, decode_responses=True, db=self.db)
        return rc

    def set_redis(self, key, value):
        self.rc.set(key, value)

    def get_all_keys(self):
        keys = self.rc.keys()
        return keys

    def get_redis(self, key):
        value = self.rc.get(key)
        return value

    def del_redis(self,key):
        self.rc.delete(key)





if __name__ == "__main__":
    re = RedisApi().get_redis(key='pre-cxm-b-controller-c2263e78-3411-11ea-a562-fad876e6a0ef')
    print (re)