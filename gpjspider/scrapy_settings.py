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
    'gpjspider.pipelines.CleanPipeline': 920,
}

DOWNLOADER_MIDDLEWARES = {
    # 'gpjspider.downloaders.FilterReduplicatedMiddleware': 1,  # 去重
    'gpjspider.downloaders.ProxyMiddleware': 100,
    'gpjspider.downloaders.SeleniumDownloader': 110,
    'gpjspider.downloaders.CurlDownloader': 119,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
ROBOTSTXT_OBEY = True

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# cookie 控制
COOKIES_ENABLED = True
COOKIES_DEBUG = DEBUG


# 并发控制
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 150
DOWNLOAD_DELAY = 0.2
RANDOMIZE_DOWNLOAD_DELAY = True

# 性能调优
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.2
AUTOTHROTTLE_MAX_DELAY = 20
AUTOTHROTTLE_DEBUG = DEBUG


#==============================================================================
# 自定义配置
#==============================================================================

#  代理
PROXIES = [
    'http://gaoge:gaoge911911@us-il.proxymesh.com:31280',
    'http://gaoge:gaoge911911@us.proxymesh.com:31280',
    'http://gaoge:gaoge911911@open.proxymesh.com:31280',
]

# 使用 selenium
SELENIUM_DOMAINS = [
    'cn2che.com',
    # 'iautos.cn',
]

# 重复性过滤
DUPEFILTER_DEBUG = DEBUG
DUPEFILTER_CLASS = 'gpjspider.contrib.dupefilter.DomainRequestDupeFilter'
JOBDIR = './data'

#  重复性过滤
FILTER_REDUPLICATED_DOMAINS = (
    "haoche51.com",
)

# 每次清理 item 的数量，清理之前会缓存在 spider 进程中
CLEAN_ITEM_CACHE_NUM = 30


#==============================================================================
# 数据库配置
#==============================================================================
# 测试配置
if DEBUG:
    MYSQL_SQLALCHEMY_URL = {
        'drivername':   'mysql+mysqldb',
        'username':     'pingjia',
        'password':     'De32wsxc',
        'host':         '101.251.105.186',
        'port':         '3306',
        'database':     'pingjia',
        'query':        {'charset': 'utf8'},
        #  mysql timeout 为 600，pool_recycle为create_engine的参数，不属于 URL。
        'pool_recycle': 550
    }
# 正式配置
else:
    MYSQL_SQLALCHEMY_URL = {
        'drivername':    'mysql+mysqldb',
        'username':      'pingjia',
        'password':      'De32wsxc',
        'host':          '211.149.206.212',
        'port':          '3306',
        'database':      'pingjia',
        'query':         {'charset': 'utf8'},
        #  mysql timeout 为 600，pool_recycle为create_engine的参数，不属于 URL。
        'pool_recycle':  550
    }


#==============================================================================
# REDIS配置
#==============================================================================
REDIS_CONFIG = [
    {"host": "192.168.168.237", "port": "6379"},
    {"host": "192.168.190.122", "port": "6379"},
    {"host": "192.168.168.237", "port": "6380"}
]
