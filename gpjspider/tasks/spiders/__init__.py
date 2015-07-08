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
import time
import shutil


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
    pidfile = os.path.join(self.log_dir, domain + '.pid')
    pid = str(os.getpid())
    # pidfile = self.log_dir + '/pid_' + domain
    # pidfile = self.log_dir + '/pid_' + spider_class.name + '.pid'

    scrapy_setting = get_project_settings()
    scrapy_setting.set('LOG_ENABLED', True, priority='cmdline')
    scrapy_setting.set('LOG_FILE', logfile, priority='cmdline')
    scrapy_setting.set('LOG_LEVEL', self.log_level.upper(), priority='cmdline')
    jobdir = os.path.join(scrapy_setting.get('JOBDIR'), domain)
    # job_queue = os.path.join(jobdir, 'requests.queue')
    is_full = rule_name.startswith('full')
    # if has one process run..
    has_run = os.path.exists(pidfile)
    jobdir2 = None
    if has_run:
        if is_full:
            time.sleep(30)
        if domain in ('ganji.com', '58.com', 'taoche.com'): # 58.com 'baixing.com', 
            print 'already run..'
            return
        if os.path.exists(jobdir):
            jobdir2 = '%s.%s' % (jobdir, pid)
            # jobdir2 = jobdir + pid
            os.makedirs(jobdir2)
            os.system('ln -s %s{,.%s}/requests.seen' % (jobdir, pid))
            jobdir = jobdir2
    # if os.path.exists(job_queue):
    #     shutil.rmtree(job_queue)
    # if os.path.exists(jobdir):
    #     shutil.rmtree(jobdir)

    scrapy_setting.set('JOBDIR', jobdir, priority='cmdline')
    crawler_process = CrawlerProcess(scrapy_setting)
    crawler = crawler_process.create_crawler()
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
        if not has_run:
            os.remove(pidfile)
        elif jobdir2:
            shutil.rmtree(jobdir2)


@app.task(name="run_full_spider", bind=True, base=GPJSpiderTask)
def run_full_spider(self, rule_name):
    logger = None
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
    logger = None
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
    logger = None
    spider_name = 'update'
    spider_class_name = '{0}AutoSpider'.format(
        spider_name.lower().capitalize())
    spider_name = spider_name + '.' + rule_name
    spider_class = create_update_spider_class(spider_class_name, spider_name)
    logfile = self.log_dir + '/{0}.log'.format(spider_class.name)
    rule = import_update_rule(rule_name)
    crawl(self, logger, logfile, spider_class, rule, rule_name)
