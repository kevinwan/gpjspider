#-*- coding:utf-8 -*-
from rediscluster import RedisCluster
import redis
# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from gpjspider.celery_settings import REDIS_CLUSTERS
from gpjspider.scrapy_settings import MYSQL_SQLALCHEMY_URL, LOCAL_REDIS, REDIS_CONFIG
import sqlalchemy as sa


def handle_checkout_event(dbapi_con, con_record, con_proxy):
    try:
        with dbapi_con.cursor() as cur:
            cur.execute("SELECT 1")
            # cur.fetchone()
    except Exception as e:
        raise sa.exc.DisconnectionError()


def get_redis_cluster():
    """
    返回一个 redis 集群的连接
    """
    return RedisCluster(startup_nodes=REDIS_CLUSTERS)


def get_local_redis():
    local_redis = REDIS_CONFIG[0]
    return redis.StrictRedis(**local_redis)
    return redis.StrictRedis(host='127.0.0.1', port=6379)

if LOCAL_REDIS:
    get_redis_cluster = get_local_redis
__engine = None
from sqlalchemy.pool import NullPool


def get_mysql_engine():
    global __engine
    if not __engine:
        # timeout = MYSQL_SQLALCHEMY_URL.pop('pool_recycle', 300)
        # timeout = 4
        # timeout = 10
        # timeout = 3600
        url = URL(**MYSQL_SQLALCHEMY_URL)
        __engine = sa.create_engine(
            url, echo_pool=False, echo=False,
            # poolclass=NullPool,
            # pool_recycle=timeout,
            # pool_timeout=0,
            pool_size=20,
            max_overflow=10,
        )
        sa.event.listen(__engine, 'checkout', handle_checkout_event)
    return __engine


def get_mysql_connect():
    return sessionmaker(bind=get_mysql_engine())


def get_mysql_cursor(session=None):
    # return session and session.connection() or get_mysql_engine().connect()
    return session.connection() if session else get_mysql_engine().connect()
