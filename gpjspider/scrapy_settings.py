# -*- coding: utf-8 -*-

DEBUG = False

BOT_NAME = 'gpjspider'

SPIDER_MODULES = ['gpjspider.spiders']
NEWSPIDER_MODULE = 'gpjspider.spiders'

ITEM_PIPELINES = {
    # 基本转换
    # 'gpjspider.pipelines.BasePipeline': 1,
    # 优质二手车的第一个 pipeline
    # 'gpjspider.pipelines.ProcessUsedCarPipeline': 500,
    # 打印
    # 'gpjspider.pipelines.save_to_db.DebugPipeline': 998,
    # 保存到数据库
    'gpjspider.pipelines.save_to_db.SaveToMySQLBySqlalchemyPipeline': 899,
    'gpjspider.pipelines.CachedCarsPipeline': 900,
    # 'gpjspider.pipelines.CleanPipeline': 920,
}

DOWNLOADER_MIDDLEWARES = {
    # 'gpjspider.downloaders.FilterReduplicatedMiddleware': 1,  # 去重
    'gpjspider.downloaders.ProxyMiddleware': 100,
    # 'gpjspider.downloaders.SeleniumDownloader': 110,
    # 'gpjspider.downloaders.CurlDownloader': 119,
    'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
}
COMPRESSION_ENABLED = True
DOWNLOAD_TIMEOUT = 30
DOWNLOAD_TIMEOUT = 60
RETRY_ENABLED = False
REDIRECT_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the
# user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# cookie 控制
COOKIES_ENABLED = False
# COOKIES_DEBUG = DEBUG


# 并发控制
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 150
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
DOWNLOAD_DELAY = 0.25
# DOWNLOAD_DELAY = 1.75
# DOWNLOAD_DELAY = 1.5
# DOWNLOAD_DELAY = 2
# DOWNLOAD_DELAY = 3.2
# DOWNLOAD_DELAY = 4
# RANDOMIZE_DOWNLOAD_DELAY = True

# 性能调优
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.25
AUTOTHROTTLE_START_DELAY = 1.25
AUTOTHROTTLE_MAX_DELAY = 20
# AUTOTHROTTLE_DEBUG = DEBUG


#==============================================================================
# 自定义配置
#==============================================================================

#  代理
PROXY_USER_PASSWD = ['gaoge:gaoge911911', ]
PROXIES = [
    'http://us-il.proxymesh.com:31280',
    'http://us.proxymesh.com:31280',
    # 'http://open.proxymesh.com:31280',
]
PROXY_DOMAINS = [
    '58.com',
    'ganji.com',
    'baixing.com',
]

# for depth crawl
SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None,
    'gpjspider.contrib.depth.DomainDepthMiddleware': 900,
}
DOMAIN_DEPTHS = {
    'ganji.com': 4,
    '58.com': 4,
    'xin.com': 5,
    'ygche.com.cn': 2,
    'renrenche.com': 2,
    'souche.com': 2,
    'haoche51.com': 2,
    # '51auto.com': 1,
}
DOMAIN_FULL_DEPTHS = {
    '58.com': 15,
    'haoche51.com': 5,
    # 'souche.com': 4,
    'xin.com': 20,
    # 'ygche.com.cn': 1,
}
DEPTH_LIMIT = 2

# 使用 selenium
SELENIUM_DOMAINS = [
    # 'cn2che.com',
    # 'taoche.com',
    # 'iautos.cn',
]

# 重复性过滤
DUPEFILTER_DEBUG = DEBUG
DUPEFILTER_CLASS = 'gpjspider.contrib.dupefilter.DomainRequestDupeFilter'
JOBDIR = '/home/gpjspider/projects/data'

#  重复性过滤
FILTER_REDUPLICATED_DOMAINS = (
    # "haoche51.com",
)

# 每次清理 item 的数量，清理之前会缓存在 spider 进程中
CLEAN_ITEM_CACHE_NUM = 30


#==============================================================================
# 数据库配置
#==============================================================================
MYSQL_SQLALCHEMY_URL = {
    'drivername':   'mysql+mysqldb',
    'username':     'pingjia',
    'password':     'De32wsxC',
    # 'host':         '211.149.206.212',
    # 'port':         '3306',
    'host':         '192.168.214.46',
    'port':          '8066',
    'database':     'pingjia',
    'query':        {'charset': 'utf8'},
}


#==============================================================================
# REDIS配置
#==============================================================================
LOCAL_REDIS = False
REDIS_CONFIG = [
    # {"host": "192.168.168.237", "port": "6379"},
    {"host": "192.168.190.122", "port": "6379"},
    {"host": "192.168.168.237", "port": "6380"},
    {"host": "192.168.168.237", "port": "6381"},
]

try:
    from local_settings import *
except ImportError:
    pass
