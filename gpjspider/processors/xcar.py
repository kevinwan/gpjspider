#!/usr/bin/env python
#-*-coding:utf-8-*-
""" xcar 处理器 """
import re
import math
from gpjspider.utils.constants import *

def model_slug(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        brand = value[0].split(u'二手')[-1]
        model = value[1].split(u'二手')[-1]
        if brand not in [u'本田', u'丰田', u'马自达', u'凯迪拉克', u'大众'] and brand in model:
            return model.split(brand)[-1]
        return model
    return value


def source_type(value):
    if value == SOURCE_TYPE_GONGPINGJIA:
        return SOURCE_TYPE_GONGPINGJIA
    return SOURCE_TYPE_ODEALER


def volume(value):
    if len(value) > 7:
        value = re.sub(ur'\d+(\.\d+)? *((万公里)|(公里)|里|万)','',value)
        value = re.sub(ur'\d+(\.\d+)?(Li)','',value)
    search = re.search(ur'^ *(\d+\.?\d*)[mMlLtT升]+', value) or re.search(ur' (\d+\.\d+)[mMlLtT升]+', value) or re.search(ur'(\d+\.\d+)[mMlLtT升]+', value) or re.search(ur' (\d+\.\d+) +', value) or re.search(ur'(\d+\.\d+) +', value) or re.search(ur'(\d+\.\d+)+', value) or re.search(ur' (\d+\.?\d*)[mMlLtT升] +', value)
    if search:
        val = search.group(1)
        if float(val) > 100:
            val = float(val)
            val = math.ceil(val / 100.0)
            return str(val / 10.0)
        else:
            return str(float(val))
    return 'temp'
