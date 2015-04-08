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
    'gpjspider.pipelines.save_to_db.SaveToMySQLBySqlalchemyPipeline': 999,
}

DOWNLOADER_MIDDLEWARES = {
    # 'gpjspider.downloaders.FilterReduplicatedMiddleware': 1,  # 去重
    'gpjspider.downloaders.ProxyMiddleware': 100,
    'gpjspider.downloaders.SeleniumDownloader': 110,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit'
    '/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
)

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# cookie 控制
COOKIES_ENABLED = True
COOKIES_DEBUG = DEBUG


# 并发控制
CONCURRENT_REQUESTS_PER_DOMAIN = 50
CONCURRENT_REQUESTS_PER_IP = 20
DOWNLOAD_DELAY = 2.3
RANDOMIZE_DOWNLOAD_DELAY = True

# 性能调优
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_MAX_DELAY = 30
AUTOTHROTTLE_DEBUG = DEBUG


#==============================================================================
# 自定义配置
#==============================================================================
# 使用 selenium
SELENIUM_DOMAINS = [
    'cn2che.com',
    # 'iautos.cn',
]

# 重复性过滤
DUPEFILTER_DEBUG = DEBUG
JOBDIR = './data'

#  重复性过滤
FILTER_REDUPLICATED_DOMAINS = (
    "haoche51.com",
)


#==============================================================================
# 数据库配置
#==============================================================================
# 测试配置
if DEBUG:
    MYSQL_SQLALCHEMY_URL = {
        'drivername': 'mysql+mysqldb',
        'username':   'pingjia',
        'password':   'De32wsxc',
        'host':       '101.251.105.186',
        'port':       '3306',
        'database':   'pingjia',
        'query':      {'charset': 'utf8'}
    }
# 正式配置
else:
    MYSQL_SQLALCHEMY_URL = {
        'drivername': 'mysql+mysqldb',
        'username':   'pingjia',
        'password':   'De32wsxc',
        'host':       '211.149.206.212',
        'port':       '3306',
        'database':   'pingjia',
        'query':      {'charset': 'utf8'}
    }


#==============================================================================
# REDIS配置
#==============================================================================
REDIS_CONFIG = [
    {"host": "192.168.168.237", "port": "6379"},
    {"host": "192.168.190.122", "port": "6379"},
    {"host": "192.168.168.237", "port": "6380"}
]
