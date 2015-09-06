#!/usr/bin/env python
#-*-coding:utf-8-*-
""" hx2car 处理器 """
import re
from gpjspider.utils.constants import *

def color(value):
    """ 【宁波】2009年11月 宝马 宝马7系 750Li 4.4T 尊贵型 香槟色 自动档 """
    value = value[0]
    val = value.split()[-2]
    if u'色' in val:
        return val
    return ''

def control(value):
    """ 【宁波】2009年11月 宝马 宝马7系 750Li 4.4T 尊贵型 香槟色 自动档 """
    value = value[0]
    return value.split()[-1]

def phone(value):
    """
        4008-900-571转130171
        15821069536  15821069536
    """
    value = value[0].strip()
    p = value.strip().split()
    if len(p) == 2:
        p1, p2 = p
        if p1.strip() == p2.strip():
            return p1
    return value.strip()


def source_type(value):
    if value == SOURCE_TYPE_GONGPINGJIA:
        return SOURCE_TYPE_GONGPINGJIA
    return SOURCE_TYPE_ODEALER


def volume(value):
    if len(value) < 7:
        search = re.search(ur'\d+(\.\d+)?', value)
        if search:
            val = search.group(0)
            return str(float(val))
    else:
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
