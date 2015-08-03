# -*- coding: utf-8 -*-
"""
专属赶集好车的 processor
"""
from decimal import Decimal


def brand_slug(value):
    """
    例子：
    1. 检测车型：马自达-马自达3星骋-1.6 手动 舒适型 2011款
    """
    if value.startswith(u'检测车型'):
        value = value.strip(u'检测车型：')
    return value.split('-')[0]


def model_slug(value):
    """
    例子：
    1. 检测车型：马自达-马自达3星骋-1.6 手动 舒适型 2011款
    """
    # if value.startswith(u'检测车型'):
        # value = value.strip(u'检测车型：')
    # return value.split('-')[1]
    value = value.replace(u'-两厢-','')
    value = value.replace(u'-三厢-','')
    return value.strip('-')


def city_slug(value):
    """
    例子：
    1. /cd/
    """
    return value.strip('/')


def price_bn(value):
    v = value.strip().strip(u'万')
    try:
        return Decimal(v)
    except:
        return 0

