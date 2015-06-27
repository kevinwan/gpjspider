#!/usr/bin/env python
#-*-coding:utf-8-*-
""" 51auto 处理器 """
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
