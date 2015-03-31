# -*- coding: utf-8 -*-

# Scrapy settings for gpjspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import django
django.setup()

BOT_NAME = 'gpjspider'

SPIDER_MODULES = ['gpjspider.spiders']
NEWSPIDER_MODULE = 'gpjspider.spiders'


ITEM_PIPELINES = {
    # 基本转换
    'gpjspider.pipelines.BasePipeline': 1,
    # 优质二手车的第一个 pipeline
    'gpjspider.pipelines.ProcessUsedCarPipeline': 500,
    # 打印
    'gpjspider.pipelines.GpjspiderPipeline': 998,
    # 保存到数据库
    # 'gpjspider.pipelines.SaveToMySQLPipeline': 999,
}

DOWNLOADER_MIDDLEWARES = {
    'gpjspider.downloaders.FilterReduplicatedMiddleware': 1,  # 去重
    'gpjspider.downloaders.ProxyMiddleware': 100,
    'gpjspider.downloaders.SeleniumDownloader': 110,
}


CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 3.3
RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit'
    '/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
)

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'


SELENIUM_DOMAINS = [
    'cn2che.com',
    # 'iautos.cn',
]


#  重复性过滤
FILTER_REDUPLICATED_DOMAINS = (
    "haoche51.com",
)
