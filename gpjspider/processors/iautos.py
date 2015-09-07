#!/usr/bin/env python
#-*-coding:utf-8-*-
from gpjspider.utils.constants import *
import re

def has_or_not(value):
    """ 齐全  - """
    if u'齐全' in value:
        return u'有'
    else:
        return u'无'

def is_certifield_car(value):
    if u'厂商认证' in value:
        return True
    else:
        return False

def source_type(value):
    if len(value) == 1:
        return SOURCE_TYPE_GONGPINGJIA # 个人车源
    elif u'厂商认证' in value[0]:
        return SOURCE_TYPE_MANUFACTURER
    else:
        return SOURCE_TYPE_ODEALER # 一般商家车

def quality_service(value):
    if isinstance(value, (list, tuple)):
        for val in value[:]:
            if u'免费代办' in val:
                value.remove(val)
            if u'贷款' in val:
                value.remove(val)
        return ' '.join(value)
    return ''

def volume(value):
    u'''
>>> volume(u'大众途观 1.8T 手自一体 豪华')
1.8
>>> volume(u'2004款北京现代酷派跑车，原装发动机，2.7排量')
2.7
    '''
    if u'万公里' in value:
        value = re.sub(ur'(\d+(\.\d+)?)万公里', '', value)
    return value


def status(value):
    if value != 'Y':
        return 'Q'
    else:
        return 'Y'
