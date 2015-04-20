# -*- coding: utf-8 -*-
"""
公平价新爬虫调度
"""
import os
from kombu import Exchange, Queue
from celery.schedules import crontab
# from datetime import timedelta


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
    {"host": "192.168.168.237", "port": "6379"},
    {"host": "192.168.190.122", "port": "6379"},
    {"host": "192.168.168.237", "port": "6380"}
]


#==============================================================================
# celery 配置
#==============================================================================
class GPJRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
        if task.startswith('run_'):
            return {'exchange': 'spiders', 'routing_key': 'spiders'}
        elif task.startswith('clean'):
            return {'exchange': 'clean', 'routing_key': 'clean'}
        elif task.startswith('qiniu'):
            return {'exchange': 'qiniu', 'routing_key': 'qiniu'}
        else:
            return {'exchange': 'default', 'routing_key': 'default'}

CELERY_QUEUES = (
    Queue('spiders', Exchange('spiders'), routing_key='spiders'),
    Queue('clean', Exchange('clean'), routing_key='clean'),
    Queue('qiniu', Exchange('qiniu'), routing_key='qiniu'),
    Queue('default', Exchange('default'), routing_key='default')
)
CELERY_TASK_RESULT_EXPIRES = 10
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_ENABLE_UTC = True
UTC_ENABLE = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'pickle'
CELERYD_CONCURRENCY = 40  # 多个进程并行处理
CELERYD_MAX_TASKS_PER_CHILD = 200
CELERY_IMPORTS = (
    "gpjspider.tasks.spiders",
    "gpjspider.tasks.clean",
    "gpjspider.tasks.qiniu",
    "gpjspider.tasks.utils",
)


BROKER_URL = "redis://192.168.190.122:6000/2"
CELERYD_TASK_LOG_LEVEL = 'INFO'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_ROUTES = (GPJRouter(),)


CELERYBEAT_SCHEDULE = {
    # "heartbeat": {
    #     'task': 'open.tasks.heartbeat_a',
    #     'schedule': timedelta(minutes=1),
    # },
    #==========================================================================
    # 优质二手车爬取新车源
    #==========================================================================
    "renrenche_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='21', minute='46'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "renrenche"},
    },
    "99haoche_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='22', minute='56'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "99haoche"},
    },
    "ganjihaoche_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='20', minute='13'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "ganjihaoche"},
    },
    "cheyipai_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='21', minute='33'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "cheyipai"},
    },
    "xin_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='22', minute='28'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "xin"},
    },
    "souche_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='20', minute='16'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "souche"},
    },
    "youche_hg_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='21', minute='32'),
        'args': ("high_quality_car",),
        'kwargs': {"rule_name": "youche"},
    },
    #==========================================================================
    # 优质二手车增量爬取新车源
    #==========================================================================
    "renrenche_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='16', minute=58),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_renrenche"},
    },
    "99haoche_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='5-22', minute='*/6'),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_99haoche"},
    },
    "ganjihaoche_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='5-22', minute='*/7'),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_ganjihaoche"},
    },
    "cheyipai_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='5-22', minute='*/8'),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_cheyipai"},
    },
    "xin_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='5-22', minute='*/6'),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_xin"},
    },
    "souche_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='5-22', minute='*/5'),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_souche"},
    },
    "youche_incr_car": {
        'task': 'run_spider',
        'schedule': crontab(hour='5-22', minute='*/5'),
        'args': ("incr_car",),
        'kwargs': {"rule_name": "incr_youche"},
    },

    #==========================================================================
    # 优质二手车更新旧车源
    #==========================================================================

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
