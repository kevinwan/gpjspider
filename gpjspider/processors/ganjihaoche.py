# -*- coding: utf-8 -*-
"""
专属赶集好车的 processor
"""
from decimal import Decimal
import re


def brand_slug(value):
    """
    例子：
    1. 检测车型：马自达-马自达3星骋-1.6 手动 舒适型 2011款
    """
    if value.startswith(u'检测车型'):
        value = value.strip(u'检测车型：')
    return value.split('-')[0]


def model_slug(value):
    u"""
    例子：
    1. 检测车型：
>>> model_slug(u'马自达-马自达3星骋-1.6 手动 舒适型 2011款')
u'\\u9a6c\\u81ea\\u8fbe3\\u661f\\u9a8b'
>>> model_slug(u'test-2-两厢-')
u'2'
>>> model_slug(u'test-3-三厢-')
u'3'
>>> model_slug(u'test-2-')
u'2'
>>> model_slug(u'标致-307 Cross-')
u'307 Cross'
>>> model_slug(u'123-56-56')
u'56'
>>> model_slug(u'奇瑞-旗云2-2011款1.5手动基本型')
u'\\u65d7\\u4e912'
    """
    # if value.startswith(u'检测车型'):
    # value = value.strip(u'检测车型：')
    # return value.split('-')[1]

    # value = re.sub(u'-.厢', '', value.rstrip('-'))
    # if ' ' in value:
    #     values = value.split()
    #     if re.search(ur'^\d+\.\d+[LT]?', values[1]) or re.search(ur'^-?\d{4}款?', values[1]):
    #         value = values[0]
    #     value = re.sub(ur'-?\d{4}款?.*', '', value, 1)
    #     value = value.replace(' ', '_')
    # if len(value.split()) > 1:
    #     if re.search(ur'^\d+\.\d+[LT]?', value.split()[1]) or re.search(ur'^-?\d{4}款?', value.split()[1]):
    #         value = value.split()[0]
    # value = re.sub(ur'-?\d{4}款?.*', '', value, 1)
    # if u'标致' in value.split()[0] and '307' in value.split()[0] and ('Cross' in value or 'cross' in value):
    #     value = u'标致307-Cross'
    # if len(value.split('-')) > 2:
    #     if value.split('-')[1] == value.split('-')[2]:
    #         value = value.split('-')[0] + '-' + value.split('-')[1]
    # value = value.rstrip('-').replace(' ', '-')
    # return value.strip(' -')

    # value = value.replace(' ', '-')
    return value.split('-')[1]


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


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
