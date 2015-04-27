# -*- coding: utf-8 -*-
import sys
import os
root = os.path.dirname(__file__)
sys.path.append(root)
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from gpjspider.utils.common import create_spider_class
from gpjspider.utils.path import import_rule
# import pdb


def main():
    spider_name = 'test'
    tp = 'full'		# full bm
    name = 'che168'		# ganjihaoche
    rule_name = '.'.join([tp, name])
    log_dir = '/tmp/gpjspider'
    spider_class_name = '{0}AutoSpider'.format(
        spider_name.lower().capitalize())
    spider_name = spider_name + '_' + rule_name
    spider_class = create_spider_class(spider_class_name, spider_name)
    logfile = log_dir + '/{0}.log'.format(spider_class.name)
    try:
        if os.path.exists(logfile):
            os.remove(logfile)
    except:
        pass
    scrapy_setting = get_project_settings()
    scrapy_setting.set('LOG_ENABLED', True, priority='cmdline')
    # scrapy_setting.set('LOG_FILE', logfile, priority='cmdline')
    scrapy_setting.set('LOG_LEVEL', 'INFO', priority='cmdline')
    # scrapy_setting.set('LOG_LEVEL', 'ERROR', priority='cmdline')
    # 原来使用爬虫名称作为JOBDIR的名称，在多个爬虫爬取同一个网站的情况下，
    # 使用 domain 可以减少一些请求
    # pdb.set_trace()
    rule = import_rule(rule_name)
    jobdir = os.path.join(scrapy_setting.get('JOBDIR'), rule['domain'])
    scrapy_setting.set('JOBDIR', jobdir, priority='cmdline')

    crawler_process = CrawlerProcess(scrapy_setting)
    crawler = crawler_process.create_crawler()
    crawler.spiders._spiders[spider_class.name] = spider_class
    spargs = {'rule_path': rule_name}
    spider = crawler.spiders.create(spider_class.name, **spargs)
    crawler.crawl(spider)
    crawler_process.start()
    del spider
    del crawler
    del crawler_process

if __name__ == '__main__':
    main()
