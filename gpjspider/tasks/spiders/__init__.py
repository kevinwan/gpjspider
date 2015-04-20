# -*- coding: utf-8 -*-
"""
关于爬虫调度的任务
"""
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from gpjspider.utils.common import create_spider_class
from gpjspider.utils.path import import_rule


@app.task(name="run_spider", bind=True, base=GPJSpiderTask)
def run_spider(self, spider_name, rule_name):
    """
    """
    logger = get_task_logger('run_spider')
    spider_class_name = '{0}AutoSpider'.format(spider_name.lower().capitalize())
    spider_name = spider_name + '_' + rule_name
    spider_class = create_spider_class(spider_class_name, spider_name)
    logger.debug(u'执行爬虫{0}, 规则:{1}'.format(spider_class.name, rule_name))
    logfile = self.log_dir + '/{0}.log'.format(spider_class.name)
    try:
        if os.path.exists(logfile):
            os.remove(logfile)
    except:
        logger.error(u'删除日志文件{0}失败'.format(logfile))
    scrapy_setting = get_project_settings()
    scrapy_setting.set('LOG_ENABLED', True, priority='cmdline')
    scrapy_setting.set('LOG_FILE', logfile, priority='cmdline')
    scrapy_setting.set('LOG_LEVEL', self.log_level.upper(), priority='cmdline')
    jobdir = scrapy_setting.get('JOBDIR')
    # 原来使用爬虫名称作为JOBDIR的名称，在多个爬虫爬取同一个网站的情况下，
    # 使用 domain 可以减少一些请求
    rule = import_rule(rule_name)
    jobdir = '{0}/{1}'.format(jobdir, rule['domain'])
    scrapy_setting.set('JOBDIR', jobdir, priority='cmdline')
    pidfile = self.log_dir + '/' + spider_class.name + '.pid'
    with open(pidfile, "w") as f:
        f.write(str(os.getpid()) + os.linesep)

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
    logger.info(u'爬虫{0},规则{1} 结束'.format(spider_class.name, rule_name))
    

