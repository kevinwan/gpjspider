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
from gpjspider.utils.common import create_full_spider_class
from gpjspider.utils.common import create_update_spider_class
from gpjspider.utils.common import create_incr_spider_class
from gpjspider.utils.path import import_rule, import_update_rule
from gpjspider.utils.path import import_full_rule, import_incr2_rule as import_incr_rule
import pdb


@app.task(name="run_spider", bind=True, base=GPJSpiderTask)
def run_spider(self, rule_name):
    logger = get_task_logger('run_spider')
    spider_name = 'default'
    spider_class_name = '{0}AutoSpider'.format(
        spider_name.lower().capitalize())
    spider_name = spider_name + '.' + rule_name
    spider_class = create_spider_class(spider_class_name, spider_name)
    logfile = self.log_dir + '/{0}.log'.format(spider_class.name)
    rule = import_rule(rule_name)
    crawl(self, logger, logfile, spider_class, rule, rule_name)


def crawl(self, logger, logfile, spider_class, rule, rule_name):
    domain = rule['domain']
    # pidfile = self.log_dir + '/pid_' + domain
    pidfile = os.path.join(self.log_dir, domain + '.pid')
    # pidfile = self.log_dir + '/pid_' + spider_class.name + '.pid'
    if os.path.exists(pidfile):# and domain != '58.com':
        print 'already run..'
        return
    # try:
    #     if os.path.exists(logfile):
    #         os.remove(logfile)
    # except:
    #     logger.error(u'Delete {0} failed'.format(logfile))
    scrapy_setting = get_project_settings()
    scrapy_setting.set('LOG_ENABLED', True, priority='cmdline')
    scrapy_setting.set('LOG_FILE', logfile, priority='cmdline')
    scrapy_setting.set('LOG_LEVEL', self.log_level.upper(), priority='cmdline')
    jobdir = os.path.join(scrapy_setting.get('JOBDIR'), domain)
    job_queue = os.path.join(jobdir, 'requests.queue')
    os.system('[ -e {0} ] && rm -rf {0}/*'.format(job_queue))
    scrapy_setting.set('JOBDIR', jobdir, priority='cmdline')
    crawler_process = CrawlerProcess(scrapy_setting)
    crawler = crawler_process.create_crawler()
    pid = str(os.getpid())
    name = '%s.%s' % (spider_class.name, pid)
    spider_class.name = name
    crawler.spiders._spiders[name] = spider_class
    spargs = {'rule_name': rule_name}
    spider = crawler.spiders.create(name, **spargs)
    with open(pidfile, "w") as f:
        f.write(pid + os.linesep)
    try:
        crawler.crawl(spider)
        crawler_process.start()
    except Exception as e:
        print e
    finally:
        del spider
        del crawler
        del crawler_process
        os.remove(pidfile)


@app.task(name="run_full_spider", bind=True, base=GPJSpiderTask)
def run_full_spider(self, rule_name):
    logger = None   # get_task_logger('run_full_spider')
    spider_name = 'full'
    spider_class_name = '{0}AutoSpider'.format(
        spider_name.lower().capitalize())
    spider_name = spider_name + '.' + rule_name
    spider_class = create_full_spider_class(spider_class_name, spider_name)
    logfile = self.log_dir + '/{0}.log'.format(spider_name)
    rule = import_full_rule(rule_name)
    rule_name = 'full.' + rule_name
    crawl(self, logger, logfile, spider_class, rule, rule_name)


@app.task(name="run_incr_spider", bind=True, base=GPJSpiderTask)
def run_incr_spider(self, rule_name):
    logger = None   # get_task_logger('run_incr_spider')
    spider_name = 'incr'
    spider_class_name = '{0}AutoSpider'.format(
        spider_name.lower().capitalize())
    spider_name = spider_name + '.' + rule_name
    spider_class = create_incr_spider_class(spider_class_name, spider_name)
    logfile = self.log_dir + '/{0}.log'.format(spider_class.name)
    rule = import_incr_rule(rule_name)
    crawl(self, logger, logfile, spider_class, rule, rule_name)


@app.task(name="run_update_spider", bind=True, base=GPJSpiderTask)
def run_update_spider(self, rule_name):
    """
    """
    logger = None   # get_task_logger('run_update_spider')
    spider_name = 'update'
    spider_class_name = '{0}AutoSpider'.format(
        spider_name.lower().capitalize())
    spider_name = spider_name + '.' + rule_name
    spider_class = create_update_spider_class(spider_class_name, spider_name)
    logfile = self.log_dir + '/{0}.log'.format(spider_class.name)
    rule = import_update_rule(rule_name)
    crawl(self, logger, logfile, spider_class, rule, rule_name)
