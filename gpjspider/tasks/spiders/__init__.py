# -*- coding: utf-8 -*-
"""
关于爬虫调度的任务
"""
import os
# from celery import shared_task
from scrapy.cmdline import execute
from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from scrapy.utils.project import get_project_settings


@app.task(name="run_spider", bind=True, base=GPJSpiderTask)
def run_spider(self, spider_name, rule_name):
    """
    """
    logger = get_task_logger('run_spider')
    logger.debug(u'执行爬虫{0}, 规则:{1}'.format(spider_name, rule_name))
    logfile = self.log_dir + '/{0}_{1}.log'.format(spider_name, rule_name)
    try:
        if os.path.exists(logfile):
            os.remove(logfile)
    except:
        logger.error(u'删除日志文件{0}失败'.format(logfile))
    scrapy_setting = get_project_settings()
    argv = [
        'scrapy', 'crawl', spider_name, '-a', 'rule_name={0}'.format(rule_name),
        '--logfile={0}'.format(logfile),
        '--loglevel={0}'.format(self.log_level.upper())
    ]
    execute(argv, scrapy_setting)
