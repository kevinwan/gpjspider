# -*- coding: utf-8 -*-
"""
本模块只存放最后一个 Pipeline。

- SaveToMySQLBySqlalchemy  使用 sqlalchemy 保存数据到 MySQL
- DebugPipeline  调试用，打印到屏幕上

"""
import datetime

from prettyprint import pp

from sqlalchemy.exc import IntegrityError

from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference

from scrapy.exceptions import NotConfigured, DropItem
from scrapy import log
from scrapy.contrib.exporter import BaseItemExporter

from gpjspider.models import *
from gpjspider.items import UsedCarItem, GpjspiderItem
from gpjspider.models.usedcars import UsedCar
from gpjspider.utils import get_mysql_connect

__ALL__ = (
    'SaveToMySQLBySqlalchemyPipeline', 'DebugPipeline', 'MongoDBPipeline')


def not_set(string):
    """ Check if a string is None or ''

    :returns: bool - True if the string is empty
    """
    if string is None:
        return True
    elif string == '':
        return True
    return False


class SaveToMySQLBySqlalchemyPipeline(object):

    """
    使用 sqlalchemy 保存到 MySQL。
    """

    def __init__(self, settings):
        if not settings.getdict('MYSQL_SQLALCHEMY_URL'):
            raise NotConfigured()
        self.connection_dict = settings.getdict('MYSQL_SQLALCHEMY_URL')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        """
        """
        self.Session = get_mysql_connect()

    def process_item(self, item, spider):
        """
        所有数据库类都要有 url 和 domain
        """
        klass = None
        #  调试的数据 URL 加上 DEBUG
        url = item.get('url', '')
        # DEBUG = spider.settings.getbool('DEBUG')
        # if DEBUG:
        #     url = 'DEBUG ' + url
        if isinstance(item, UsedCarItem):
            klass = UsedCar
            if item.get('dmodel') is None:
                item['dmodel'] = item['title']
        else:
            cls_name = item.__class__.__name__
            try:
                klass = eval(cls_name.replace('Item', ''))
            except:
                pass
        if not klass:
            raise DropItem(u'未找到数据库模型:{0}'.format(type(item)))
        session = self.Session()
        o = klass(**item)
        session.add(o)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            q = session.query(klass).filter(klass.url == url)
            # q = session.query(klass).filter(klass.domain == item['domain']).filter(klass.name == item['name'])
            q.update(dict(item), synchronize_session=False)
            # q = session.query(klass).filter(klass.url == url)
            item['id'] = q.first().id
            spider.log(u'成功保存:重复:{0}'.format(url))
        else:
            item['id'] = o.id
            spider.log(u'成功保存:{0}'.format(url))
        for field_name in item.fields.keys():
            item[field_name] = getattr(o, field_name)
        return item


class MongoDBPipeline(BaseItemExporter):

    """ MongoDB pipeline class """
    # Default options
    config = {
        'uri': 'mongodb://localhost:27017',
        'fsync': False,
        'write_concern': 0,
        'database': 'scrapy-mongodb',
        'collection': 'items',
        'replica_set': None,
        'unique_key': None,
        'buffer': None,
        'append_timestamp': False,
        'stop_on_duplicate': 0,
    }

    # Item buffer
    current_item = 0
    item_buffer = []

    # Duplicate key occurence count
    duplicate_key_count = 0

    def __init__(self, crawler):
        """ Constructor """
        super(MongoDBPipeline, self).__init__()
        self.settings = crawler.settings

        self.crawler = crawler

        # Configure the connection
        self.configure()

        if self.config['replica_set'] is not None:
            connection = MongoReplicaSetClient(
                self.config['uri'],
                replicaSet=self.config['replica_set'],
                w=self.config['write_concern'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY_PREFERRED)
        else:
            # Connecting to a stand alone MongoDB
            connection = MongoClient(
                self.config['uri'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY)

        # Set up the collection
        database = connection[self.config['database']]
        self.collection = database[self.config['collection']]
        log.msg(u'Connected to MongoDB {0}, using "{1}/{2}"'.format(
            self.config['uri'],
            self.config['database'],
            self.config['collection']))

        # Ensure unique index
        if self.config['unique_key']:
            self.collection.ensure_index(
                self.config['unique_key'], unique=True)
            log.msg('uEnsuring index for key {0}'.format(
                self.config['unique_key']))

        # Get the duplicate on key option
        if self.config['stop_on_duplicate']:
            tmpValue = self.config['stop_on_duplicate']
            if tmpValue < 0:
                log.msg(
                    (
                        u'Negative values are not allowed for'
                        u' MONGODB_STOP_ON_DUPLICATE option.'
                    ),
                    level=log.ERROR
                )
                raise SyntaxError(
                    (
                        'Negative values are not allowed for'
                        ' MONGODB_STOP_ON_DUPLICATE option.'
                    )
                )
            self.stop_on_duplicate = self.config['stop_on_duplicate']
        else:
            self.stop_on_duplicate = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def configure(self):
        """ Configure the MongoDB connection """
        # Handle deprecated configuration
        if not not_set(self.settings['MONGODB_HOST']):
            msg = u'DeprecationWarning: MONGODB_HOST is deprecated'
            log.msg(msg, level=log.WARNING)
            mongodb_host = self.settings['MONGODB_HOST']

            if not not_set(self.settings['MONGODB_PORT']):
                msg = u'DeprecationWarning: MONGODB_PORT is deprecated'
                log.msg(msg, level=log.WARNING)
                uri = 'mongodb://{0}:{1:i}'.format(
                    mongodb_host, self.settings['MONGODB_PORT'])
                self.config['uri'] = uri
            else:
                self.config['uri'] = 'mongodb://{0}:27017'.format(mongodb_host)

        if not not_set(self.settings['MONGODB_REPLICA_SET']):
            if not not_set(self.settings['MONGODB_REPLICA_SET_HOSTS']):
                log.msg(
                    (
                        u'DeprecationWarning: '
                        u'MONGODB_REPLICA_SET_HOSTS is deprecated'
                    ),
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}'.format(
                    self.settings['MONGODB_REPLICA_SET_HOSTS'])

        # Set all regular options
        options = [
            ('uri', 'MONGODB_URI'),
            ('fsync', 'MONGODB_FSYNC'),
            ('write_concern', 'MONGODB_REPLICA_SET_W'),
            ('database', 'MONGODB_DATABASE'),
            ('collection', 'MONGODB_COLLECTION'),
            ('replica_set', 'MONGODB_REPLICA_SET'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
            ('buffer', 'MONGODB_BUFFER_DATA'),
            ('append_timestamp', 'MONGODB_ADD_TIMESTAMP'),
            ('stop_on_duplicate', 'MONGODB_STOP_ON_DUPLICATE')
        ]

        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

        # Check for illegal configuration
        if self.config['buffer'] and self.config['unique_key']:
            log.msg(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ),
                level=log.ERROR)
            raise SyntaxError(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ))

    def process_item(self, item, spider):
        item = dict(self._get_serialized_fields(item))

        if self.config['buffer']:
            self.current_item += 1

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

            self.item_buffer.append(item)

            if self.current_item == self.config['buffer']:
                self.current_item = 0
                return self.insert_item(self.item_buffer, spider)

            else:
                return item

        return self.insert_item(item, spider)

    def close_spider(self, spider):
        if self.item_buffer:
            self.insert_item(self.item_buffer, spider)

    def insert_item(self, item, spider):
        if not isinstance(item, list):
            item = dict(item)

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

        if self.config['unique_key'] is None:
            try:
                self.collection.insert(item, continue_on_error=True)
                log.msg(
                    u'Stored item(s) in MongoDB {0}/{1}'.format(
                        self.config['database'], self.config['collection']),
                    level=log.DEBUG,
                    spider=spider)
            except errors.DuplicateKeyError:
                log.msg(u'Duplicate key found', level=log.DEBUG)
                if (self.stop_on_duplicate > 0):
                    self.duplicate_key_count += 1
                    if (self.duplicate_key_count >= self.stop_on_duplicate):
                        self.crawler.engine.close_spider(
                            spider,
                            'Number of duplicate key insertion exceeded'
                        )
                pass

        else:
            key = {}
            if isinstance(self.config['unique_key'], list):
                for k in dict(self.config['unique_key']).keys():
                    key[k] = item[k]
            else:
                key[self.config['unique_key']] = item[
                    self.config['unique_key']]

            self.collection.update(key, item, upsert=True)
            msg = u'Stored item(s) in MongoDB {0}/{1}'.format(
                self.config['database'], self.config['collection'])
            log.msg(msg, level=log.DEBUG, spider=spider)

        return item


class DebugPipeline(object):

    """
    调试用
    """

    def process_item(self, item, spider):
        if isinstance(item, GpjspiderItem):
            pp(dict(item))
        return item
