# -*- coding: utf-8 -*-
from __future__ import absolute_import
# from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask


@app.task(name="del_cached_cars", bind=True, base=GPJSpiderTask)
def del_cached_cars():
    pass
