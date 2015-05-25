# -*- coding: utf-8 -*-
"""
公平价新爬虫调度
"""
import os
from kombu import Exchange, Queue
from celery.schedules import crontab


#==============================================================================
# 七牛存储配置
#==============================================================================
QINIU_ACCESS_KEY = 'VDo2clWr4g7DJ2d1S8h_8W17d2RzmMdrywI-TiBm'
QINIU_SECRET_KEY = 'H7Axjej_QhlpgbAry4rVNyoBOnNj9etSfWYcHXi7'
QINIU_BUCKET = 'gongpingjia'


#==============================================================================
# 爬虫运行环境配置
#==============================================================================
PROJECT_DIR = os.getcwd()
LOG_DIR = '/tmp/gpjspider'
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_LEVEL = 'debug'
# 不可缺少
SCRAPY_SETTINGS = "gpjspider.scrapy_settings"
# redis 环境，和 broker 不同
REDIS_CLUSTERS = [
    {"host": "127.0.0.1", "port": "6379"},
    {"host": "192.168.190.122", "port": "6379"},
    # {"host": "127.0.0.1", "port": "6381"},
    {"host": "127.0.0.1", "port": "6380"}
]


#==============================================================================
# celery 配置
#==============================================================================
class GPJRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
        if task.startswith('run_spider'):
            return {'exchange': 'spider', 'routing_key': 'spider'}
        elif task.startswith('run_full_spider'):
            return {'exchange': 'full', 'routing_key': 'full'}
        elif task.startswith('run_update_spider'):
            return {'exchange': 'update', 'routing_key': 'update'}
        elif task.startswith('run_incr_spider'):
            return {'exchange': 'incr', 'routing_key': 'incr'}
        elif task.startswith('clean'):
            return {'exchange': 'clean', 'routing_key': 'clean'}
        else:
            return {'exchange': 'default', 'routing_key': 'default'}

CELERY_QUEUES = (
    Queue('spider', Exchange('spider'), routing_key='spider'),
    Queue('full', Exchange('full'), routing_key='full'),
    Queue('update', Exchange('update'), routing_key='update'),
    Queue('incr', Exchange('incr'), routing_key='incr'),
    Queue('clean', Exchange('clean'), routing_key='clean'),
    Queue('default', Exchange('default'), routing_key='default')
)


CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_ENABLE_UTC = True
UTC_ENABLE = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'json'
# CELERYD_CONCURRENCY = 1  # 多个进程并行处理
CELERYD_MAX_TASKS_PER_CHILD = 200
# CELERYD_MAX_TASKS_PER_CHILD = 1
CELERY_IMPORTS = (
    "gpjspider.tasks.spiders",
    "gpjspider.tasks.clean",
    "gpjspider.tasks.qiniu",
    "gpjspider.tasks.utils",
)
CELERY_TASK_RESULT_EXPIRES = 10
CELERY_RESULT_BACKEND = 'db+sqlite:///res.db'
CELERY_IGNORE_RESULT = True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

BROKER_URL = "redis://192.168.190.122:6000/2"
CELERYD_TASK_LOG_LEVEL = 'INFO'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_ROUTES = (GPJRouter(),)


CELERYBEAT_SCHEDULE = {
    #==========================================================================
    # 优质二手车爬取新车源
    #==========================================================================
    # "99haoche_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='22', minute='26'),
    #     'kwargs': {"rule_name": "99haoche"},
    # },
    # "ganjihaoche_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='22', minute='23'),
    #     'kwargs': {"rule_name": "ganjihaoche"},
    # },
    # "che168_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='22', minute='25'),
    #     'kwargs': {"rule_name": "che168"},
    # },
    # "renrenche_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='22', minute='46'),
    #     'kwargs': {"rule_name": "renrenche"},
    # },
    # "cheyipai_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='23', minute='24'),
    #     'kwargs': {"rule_name": "cheyipai"},
    # },
    # "xin_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='22', minute='58'),
    #     'kwargs': {"rule_name": "xin"},
    # },
    # "souche_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='22', minute='16'),
    #     'kwargs': {"rule_name": "souche"},
    # },
    # "youche_hg_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='23', minute='32'),
    #     'kwargs': {"rule_name": "youche"},
    # },
    # "taoche_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='15', minute='25'),
    #     'kwargs': {"rule_name": "che168"},
    # },
    # "sohu_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='15', minute='25'),
    #     'kwargs': {"rule_name": "che168"},
    # },
    # # 认证车商二手车
    # "mcc_58_car": {
    #     'task': 'run_full_spider',
    #     'schedule': crontab(hour='*/8', minute='2'),
    #     'kwargs': {"rule_name": "manufacturer_certificated_cars.58"},
    # },
    #==========================================================================
    # 优质二手车增量爬取新车源
    #==========================================================================
    # "renrenche_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "renrenche"},
    # },
    # "99haoche_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "99haoche"},
    # },
    # "ganjihaoche_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "ganjihaoche"},
    # },
    # "cheyipai_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "cheyipai"},
    # },
    # "xin_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "xin"},
    # },
    # "souche_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "souche"},
    # },
    # "youche_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "youche"},
    # },
    # "58_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*10'),
    #     'kwargs': {"rule_name": "58"},
    # },
    # "che168_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "che168"},
    # },
    # "taoche_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "taoche"},
    # },
    # "sohu_incr_car": {
    #     'task': 'run_incr_spider',
    #     'schedule': crontab(hour='5-21', minute='*/10'),
    #     'kwargs': {"rule_name": "sohu"},
    # },

    #==========================================================================
    # 辅助任务
    #==========================================================================
    #  每隔4小时，检测代理 IP 可用
    "check_proxy_ip-5h": {
        'task': 'check_proxy_ip',
        'schedule': crontab(hour='6-23/6', minute=0),
    },
    #  夜间再检测一次，检测代理 IP 可用
    "check_proxy_ip-2h": {
        'task': 'check_proxy_ip',
        'schedule': crontab(hour='3', minute=45),
    },
}
