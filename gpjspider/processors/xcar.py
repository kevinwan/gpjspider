#!/usr/bin/env python
#-*-coding:utf-8-*-
""" xcar 处理器 """
import re
from gpjspider.utils.constants import *

def model_slug(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        brand = value[0].split(u'二手')[-1]
        model = value[1].split(u'二手')[-1]
        if brand in model:
            return model.split(brand)[-1]
        return model
    return value

def status(value):
    if value == 'Q':
        return 'Q'
    return 'Y'

def source_type(value):
    if value == SOURCE_TYPE_GONGPINGJIA:
        return SOURCE_TYPE_GONGPINGJIA
    return SOURCE_TYPE_ODEALER


def volume(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            if len(value[0]) == 2:
                return value[0].strip(u'L').strip(u'T') + '.0'
    return ''
