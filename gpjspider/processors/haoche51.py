# -*- coding: utf-8 -*-
"""
专属haoche51的 processor
"""
import re


def year(value):
    """
    例子：
    1. 2011.01上牌  |  行驶8.6万公里  |   手自一体  |   南京牌照  |
        国四        排放  |  过户1次
    """
    a = value.split('|')[0]
    b = a.strip(u' 上牌').split('.')
    return b[0]


def month(value):
    """
    """
    a = value.split('|')[0]
    b = a.strip(u' 上牌').split('.')
    return b[1]


def mile(value):
    """
    """
    a = value.split('|')[1]
    b = a.strip(u' 行驶万公里')
    return b


def control(value):
    """
    """
    a = value.split('|')
    de = ''
    if u'双离合' in value or u'无级变速' in value:
        de = u'自动'
    for i in a:
        if u'手' in i or u'自' in i:
            de = i
            break
    return de.strip()


def region(value):
    value = [v.strip() for v in value.split('|')][1:]

    return ''.join(value)


def contact(value):
    return value.split('|')[0].strip()


def brand_slug(value):
    """
    例子：
    1. 雪铁龙 C5 2011款 2.3L 自动尊驭型
    """
    return value.split(' ')[0]


def model_slug(value):
    """
    例子：
    1. 雪铁龙 C5 2011款 2.3L 自动尊驭型
    """
    return value.split(' ')[1]


def city(value):
    """
    """
    a = value.split('|')
    de = ''
    for i in a:
        if u'牌照' in i:
            de = i
            break
    return de.strip().strip(u'牌照')


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


re_transfer_owner = re.compile(ur'(\d+)次')


def transfer_owner(value):
    """
    过户次数
    1. 2009.04上牌 | 行驶4.9万公里 | 手自一体 | 北京牌照 | 国四 排放 | 过户2次
    2. 过户次数: 2次
    """
    a = re_transfer_owner.findall(value)
    if a:
        return int(a[0])
    else:
        return 0


def driving_license(value):
    """
    行驶证
    """
    if u'行驶证' in value:
        return u'是' if u'有' in value else u'否'

    return None


def invoice(value):
    """
    """
    if u'购车发票/过户发票' in value:
        return u'是' if u'有' in value else u'否'
    return None


def status(value):
    if u'已成交' in value:
        return 'Q'
    else:
        return 'Y'
