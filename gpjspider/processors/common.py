# -*- coding: utf-8 -*-
from decimal import Decimal
import re

reg_blank_split = re.compile(r'\s+')


def strip(value):
    """
    如果是字符串，去除空格 \r  \n \t
    如果不是，原样返回
    """
    if not isinstance(value, basestring):
        return value
    return value.strip(' \r\n\t')


def first(value):
    """
    """
    if isinstance(value, (list, tuple)):
        return value[0]
    else:
        return value


def last(value):
    """
    """
    if isinstance(value, (list, tuple)):
        return value[-1]
    else:
        return value


def join(value):
    """
    todo:  暂时用空格 join
    """
    if isinstance(value, (list, tuple)):
        return u' '.join(value)
    else:
        return value


def strip_html(value):
    """
    """
    assert isinstance(value, basestring)
    return value.strip('<br>').strip('<br/>').strip('<br />')


def gpjint(value, default=0):
    """
    将 value 尝试转换成 int, 不成功时返回 default
    """
    try:
        value = int(value)
    except:
        return default
    else:
        return value


def gpjfloat(value, default=0.0):
    """
    将 value 尝试转换成 float, 不成功时返回 default
    """
    if isinstance(value, basestring):
        value = value.strip()
    try:
        value = float(value)
    except:
        return default
    else:
        return value


def price(value):
    """
    示例：
    ￥128.00万
    """
    v = value.strip().strip(u'￥万')
    return v


def price_bn(value):
    """
    支持的：
    1. 新车价：29.88万+2.56万（购置税）

    """
    v = value.split('+')[0]
    v = v.strip().strip(u'新车价：')
    v = v.strip().strip(u'万')
    return v


def decimal(value, default=Decimal(0)):
    """
    """
    try:
        return Decimal(value)
    except:
        return default


def year(value):
    """
    value 示例：
    1. 2007-1
    2. 2014年09月
    """
    if '-' in value:
        return value.split('-')[0]
    elif u'年' in value:
        return value.split(u'年')[0]


def month(value):
    """
    value 示例：
    1. 2007-1
    2. 2014年09月
    """
    return value.split('-')[1]
    if '-' in value:
        return value.split('-')[1]
    elif u'年' in value:
        return value.split(u'年')[1].strip().strip(u'月')


def mile(value):
    """
    0.1万公里
    """
    return value.strip().strip(u'万公里')


def brand_slug(value):
    """
    支持这样的：

    1. 奔驰  唯雅诺
    2. 起亚 >

    """
    a = reg_blank_split.split(value)
    return a[0]


def model_slug(value):
    """
    支持这样的：

    1. 奔驰  唯雅诺
    2. 兰德酷路泽 >
    """
    value = value.strip('>')
    if ' ' in value:
        a = reg_blank_split.split(value)
        return a[1]
    else:
        return value
