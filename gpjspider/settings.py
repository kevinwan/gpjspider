# -*- coding: utf-8 -*-

# Scrapy settings for gpjspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gpjspider'

SPIDER_MODULES = ['gpjspider.spiders']
NEWSPIDER_MODULE = 'gpjspider.spiders'

ITEM_PIPELINES = {
    'gpjspider.pipelines.GpjspiderPipeline': 1,

    'gpjspider.pipelines.SaveToMySQLPipeline': 999,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'gpjspider (+http://www.yourdomain.com)'
