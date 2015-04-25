# -*- coding: utf-8 -*-
from decimal import Decimal
import re

reg_blank_split = re.compile(r'\s+')
reg_volumn = re.compile(r'(\d\.\d)')


def strip(value):
    """
    如果是字符串，去除空格 \r  \n \t
    如果不是，原样返回
    """
    if not isinstance(value, basestring):
        return value
    value = value.replace(u'\xa0', u'')
    value = value.replace(u'\xb7', u'')
    value = value.replace(u'\r', u'')
    value = value.replace(u'\n', u'')
    value = value.replace(u'\t', u'')
    return value.strip(' ')


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


def join(values):
    """
    todo:  暂时用空格 join
    """
    value = [v.strip().strip('\t\r\n\b').strip() for v in values]
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


def gpjdecimal(value, default=0.0):
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
    v = value.strip().strip(u'￥万\xa5').strip()
    return decimal(v)


def price_bn(value):
    """
    支持的：
    1. 新车价：29.88万+2.56万（购置税）

    """
    v = value.split('+')[0]
    v = v.strip().strip(u'新车价：')
    v = v.strip().strip(u'万')
    return decimal(v)


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
    if '-' in value:
        return value.split('-')[1]
    elif u'年' in value:
        return value.split(u'年')[1].strip().strip(u'月')


def mile(value):
    """
    0.1万公里
    """
    return value.strip().strip(u'万公里')


def volume(value):
    """
    例子：
    1. 大众途观 1.8T 手自一体 豪华
    """
    a = reg_volumn.findall(value)
    if a:
        return decimal(a[0])
    else:
        return None


def brand_slug(value):
    """
    支持这样的：

    1. 奔驰  唯雅诺
    2. 起亚 >
    3. 菲亚特-菲翔2012款

    """
    a = value.strip('>').strip()
    a = reg_blank_split.split(a)
    if '-' in a[0]:
        a = a[0].split('-')
    return a[0].strip()


def model_slug(value):
    """
    支持这样的：

    1. 奔驰  唯雅诺
    2. 兰德酷路泽 >
    3. 菲亚特-菲翔2012款
    """
    value = value.strip('>').strip()
    if ' ' in value:
        a = reg_blank_split.split(value)
        return a[1]
    elif '-' in value:
        a = value.split('-')
        return a[1]
    else:
        return value


def city(value):
    """
    """
    return value.strip(u'市').strip(u'二手车城').strip(u'二手').strip('>')


def strip_url(url_with_query):
    """
    去除 URL 里的 querystring
    """
    if '?' in url_with_query:
        return url_with_query.split('?')[0]
    else:
        return url_with_query


def strip_imgurls(urls_with_query):
    """
    专门用于strip 掉 imgurl 的 url 中包含的 querystring
    """
    urls_with_query = urls_with_query.split()
    new_urls = []
    for url in urls_with_query:
        new_urls.append(strip_url(url))
    return ' '.join(new_urls)


g_y_m = re.compile(ur'(\d{4}).*(\d{2})')


def mandatory_insurance(value):
    """
    """
    a = g_y_m.findall(value)
    if a:
        return u'-'.join(a[0]) + u'-01'
    else:
        return u''


def business_insurance(value):
    """
    """
    a = g_y_m.findall(value)
    if a:
        return u'-'.join(a[0]) + u'-01'
    else:
        return u''


def examine_insurance(value):
    """
    """
    a = g_y_m.findall(value)
    if a:
        return u'-'.join(a[0]) + u'-01'
    else:
        return u''


def status(value):
    if value == '1':
        return 'sale'
    elif value == '0':
        return 'review'
    return 'sale'


gpjfloat = decimal
