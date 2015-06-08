# -*- coding: utf-8 -*-

DEBUG = True
DEBUG = False
DUPEFILTER_DEBUG = DEBUG
COOKIES_DEBUG = DEBUG
JOBDIR = 'data'

if DEBUG:
    # if False:
    ITEM_PIPELINES = {
        'gpjspider.pipelines.save_to_db.DebugPipeline': 998,
        # 'gpjspider.pipelines.save_to_db.SaveToMySQLBySqlalchemyPipeline': 899,
        # 'gpjspider.pipelines.CachedCarsPipeline': 900,
        # 'gpjspider.pipelines.CleanPipeline': 920,
    }
    DOWNLOADER_MIDDLEWARES = {
        # 'gpjspider.downloaders.RFPDupeFilter': 1,  # 去重
        #'gpjspider.downloaders.ProxyMiddleware': 100,
        # 'gpjspider.downloaders.SeleniumDownloader': 110,
        # 'gpjspider.downloaders.CurlDownloader': 119,
        'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
        'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
    }
    SELENIUM_DOMAINS = [
        # 'cn2che.com',
    ]
else:
    ITEM_PIPELINES = {
        'gpjspider.pipelines.save_to_db.SaveToMySQLBySqlalchemyPipeline': 899,
        'gpjspider.pipelines.CachedCarsPipeline': 900,
        # 'gpjspider.pipelines.CleanPipeline': 920,
    }
    DOWNLOADER_MIDDLEWARES = {
        #'gpjspider.downloaders.ProxyMiddleware': 100,
        'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    }
    DOWNLOAD_DELAY = 2

DOWNLOAD_TIMEOUT = 15
CONCURRENT_REQUESTS_PER_DOMAIN = 20
CONCURRENT_REQUESTS_PER_IP = 10

LOCAL_REDIS = True
REDIS_CONFIG = [
    {"host": "127.0.0.1", "port": "6379"},
]

MYSQL_SQLALCHEMY_URL = {
    'drivername': 'mysql+mysqldb',
    'username': 'pingjia',
    'password': 'De32wsxc',
    'host': '101.251.105.186',
    'port': '3306',
    'host': '211.149.214.46',
    'port': '8066',
    'database': 'pingjia',
    'query': {'charset': 'utf8'},
}
