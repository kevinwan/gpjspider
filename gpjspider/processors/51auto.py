#!/usr/bin/env python
#-*-coding:utf-8-*-
""" 51auto 处理器 """
import re
from gpjspider.utils.constants import *


def price_bn(value):
    """ 新车最低价499.21万[含购置税39.31万] """
    prices = re.findall('\d+\.?\d*', value)
    if len(prices) == 2:
        all_price, tax = prices
        return str(float(all_price) - float(tax))
    # return ''


def control(value):
    """ 关键参数：手自一体 5.9L """
    """关键参数：手自一体2.0L"""
    value = value.strip()
    contr = re.search(u'关键参数：([\u4E00-\u9FA5]+)\d\.?\d?[LT]', value)
    if ' ' in value:
        return value.split(u'：')[-1].split()[0]
    elif contr:
        return contr.groups()[0]
    else:
        return value


def imgurls(value):
    """ 去掉图片中包含 mid 的图片 """
    if isinstance(value, (list, tuple)):
        for img in value[:]:
            if img.find('-mid') != -1:
                value.remove(img)
        return ' '.join(value)

    return value


def color(value):
    color_base = (
        u'黑色',
        u'白色',
        u'灰色',
        u'咖啡色',
        u'红色',
        u'蓝色',
        u'绿色',
        u'黄色',
        u'橙色',
        u'香槟色',
        u'紫色',
        u'多彩色',
        u'银色',
    )

    for c in color_base:
        if c in value:
            return c
    return ''


def source_type(value):
    type_base = (
        (u'品牌', SOURCE_TYPE_MANUFACTURER),
        (u'商家', SOURCE_TYPE_SELLER),
        (u'个人', SOURCE_TYPE_GONGPINGJIA),
    )

    for t in type_base:
        if t[0] in value:
            return t[1]

    return SOURCE_TYPE_ODEALER
