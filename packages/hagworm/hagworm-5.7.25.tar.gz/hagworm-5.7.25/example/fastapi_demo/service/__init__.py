# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from hagworm.extend.trace import get_trace_id
from hagworm.extend.error import Ignore, catch_error
from hagworm.extend.metaclass import Singleton
from hagworm.extend.asyncio.base import Utils, FuncCache, ShareFuture
from hagworm.extend.asyncio.task import MultiTasks
from hagworm.extend.asyncio.redis import RedisDelegate
from hagworm.extend.asyncio.mongo import MongoDelegate
from hagworm.extend.asyncio.mysql import MySQLDelegate
from hagworm.extend.process import HeartbeatChecker

from setting import Config


class DataSource(Singleton, RedisDelegate, MongoDelegate, MySQLDelegate):

    def __init__(self):

        RedisDelegate.__init__(self)
        MongoDelegate.__init__(self)
        MySQLDelegate.__init__(self)

        self._health_checker = HeartbeatChecker(Config.ServerName)

    @classmethod
    async def initialize(cls):

        inst = cls()

        (await inst.init_redis_single(
            Config.RedisHost[0], Config.RedisHost[1], password=Config.RedisPasswd,
            min_connections=Config.RedisMinConn, max_connections=Config.RedisMaxConn
        )).set_key_prefix(Config.RedisKeyPrefix)

        inst.init_mongo(
            Config.MongoHost, Config.MongoUser, Config.MongoPasswd,
            auth_source=Config.MongoAuth,
            min_pool_size=Config.MongoMinConn, max_pool_size=Config.MongoMaxConn, max_idle_time=3600
        )

        if Config.MySqlMasterServer:

            await inst.init_mysql_rw(
                Config.MySqlMasterServer[0], Config.MySqlMasterServer[1], Config.MySqlName,
                Config.MySqlUser, Config.MySqlPasswd,
                minsize=Config.MySqlMasterMinConn, maxsize=Config.MySqlMasterMaxConn,
                echo=Config.Debug, pool_recycle=21600, conn_life=43200
            )

        if Config.MySqlSlaveServer:

            await inst.init_mysql_ro(
                Config.MySqlSlaveServer[0], Config.MySqlSlaveServer[1], Config.MySqlName,
                Config.MySqlUser, Config.MySqlPasswd,
                minsize=Config.MySqlSlaveMinConn, maxsize=Config.MySqlSlaveMaxConn,
                echo=Config.Debug, pool_recycle=21600, readonly=True, conn_life=43200
            )

    @classmethod
    async def release(cls):

        inst = cls()

        inst._health_checker.release()

        inst.close_mongo_pool()

        await inst.close_redis_pool()

    @classmethod
    async def check_health(cls):

        return await cls().health()

    @property
    def online(self):

        return self._health_checker.check()

    @ShareFuture()
    @FuncCache(ttl=30)
    async def health(self):

        result = False

        with catch_error():

            tasks = MultiTasks()

            tasks.append(self.redis_health())
            tasks.append(self.mysql_health())
            tasks.append(self.mongo_health())

            await tasks

            result = all(tasks)

            if result is True:
                self._health_checker.refresh()

        return result


class ServiceBase(Singleton, Utils):

    def __init__(self):

        self._data_source = DataSource()

    @property
    def trace_id(self):

        return get_trace_id()

    def Break(self, *args, layers=1):

        raise Ignore(*args, layers=layers)
