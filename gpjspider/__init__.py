# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery
from celery.task import Task


celery_app = Celery('gpjspider')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
celery_app.config_from_object('gpjspider.celery_settings')


class GPJTask(Task):
    """
    """
    abstract = True


class GPJSpiderTask(GPJTask):
    """
    """

    def __init__(self):
        """
        """
        os.environ['SCRAPY_SETTINGS_MODULE'] = self.app.conf.SCRAPY_SETTINGS
        self.project_dir = self.app.conf.PROJECT_DIR
        self.log_dir = self.app.conf.LOG_DIR
        self.log_level = self.app.conf.LOG_LEVEL
