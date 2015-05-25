#-*- coding:utf-8 -*-
from rediscluster import RedisCluster
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from gpjspider.celery_settings import REDIS_CLUSTERS
from gpjspider.scrapy_settings import MYSQL_SQLALCHEMY_URL, LOCAL_REDIS


def get_redis_cluster():
    """
    返回一个 redis 集群的连接
    """
    return RedisCluster(startup_nodes=REDIS_CLUSTERS)


def get_local_redis():
    return redis.StrictRedis(host='127.0.0.1', port=6379)

if LOCAL_REDIS:
    get_redis_cluster = get_local_redis
__engine = None


def get_mysql_engine():
    global __engine
    if not __engine:
        timeout = MYSQL_SQLALCHEMY_URL.pop('pool_recycle', 300)
        url = URL(**MYSQL_SQLALCHEMY_URL)
        __engine = create_engine(url, pool_recycle=timeout, pool_size=20, max_overflow=100, echo_pool=False)
    return __engine


def get_mysql_connect():
    return sessionmaker(bind=get_mysql_engine())

__cursor = None
def get_mysql_cursor():
    return get_mysql_engine().connect()
    global __cursor
    if not __cursor:
        __cursor = get_mysql_engine().connect()
    return __cursor
