#!/usr/bin/env python
#-*-coding:utf-8-*-
import re
import math
from gpjspider.utils.constants import *

def volume(value):
    """ 1588ml 6.7L 9.726L """
    # match = re.match('(\d+\.?\d*)[mMlL]+', value)
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

def status(value):
    if u'删除' in value:
        return 'Q'
    else:
        return 'Y'

def source_type(value):
    if u'车商' in value:
        return SOURCE_TYPE_ODEALER
    else:
        return SOURCE_TYPE_GONGPINGJIA

def dmodel(value):
    """
        【宜春】二手自卸车东风柳汽 霸龙   8x2 前二后八  价格26.50万
        【宁波】奔驰 G级 G500-5.5-AT四驱 价格122.00万
    """
    val = value.split(u'】')[-1].split(u'价')[0]
    return val.replace(u'二手', '')
