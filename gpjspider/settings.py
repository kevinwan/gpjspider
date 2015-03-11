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
    # 'gpjspider.pipelines.GpjspiderPipeline': 1,

    'gpjspider.pipelines.SaveToMySQLPipeline': 999,
}

DOWNLOADER_MIDDLEWARES = {
    # 'gpjspider.downloaders.ProxyMiddleware': 100,
    'gpjspider.downloaders.SeleniumDownloader': 110,
}


CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2.5
RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit'
    '/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
)


SELENIUM_DOMAINS = [
    'cn2che.com',
    'iautos.cn',
]
