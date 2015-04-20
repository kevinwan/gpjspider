#-*- coding:utf-8 -*-
from rediscluster import RedisCluster
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from gpjspider.celery_settings import REDIS_CLUSTERS
from gpjspider.scrapy_settings import MYSQL_SQLALCHEMY_URL


def get_redis_cluster():
    """
    返回一个 redis 集群的连接
    """
    return RedisCluster(startup_nodes=REDIS_CLUSTERS)


__engine = None


def get_mysql_connect():
    """
    """
    global __engine
    if not __engine:
        timeout = MYSQL_SQLALCHEMY_URL.pop('pool_recycle', 300)
        url = URL(**MYSQL_SQLALCHEMY_URL)
        __engine = create_engine(url, pool_recycle=timeout, pool_size=40)
    Session = sessionmaker(bind=__engine)
    return Session
