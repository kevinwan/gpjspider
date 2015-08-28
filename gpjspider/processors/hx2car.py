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
