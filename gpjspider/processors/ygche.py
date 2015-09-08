#-*-coding:utf-8-*-
import re


def color(value):
    """ 2010款 凯美瑞三厢 240G 豪华版 手自一体 黑色"""
    val = value.split()[-1]
    if u'色' in val:
        return val
    return ''


def price_bn(value):
    """ ￥24.62万（含￥1.94万购置税）"""
    price = re.findall('\d+\.?\d*', value)
    return str(float(price[0]) - float(price[1]))


def has_or_not(value):
    if value.strip().lower() == 'yes':
        return u'有'
    return u'无'


def condition_level(value):
    """
        优+ -> Excellent -> A+
        优 -> good  -> A
        良 -> well -> B
        中 -> fair -> C
    """
    value = value.strip().lower()

    if value == 'excellent':
        return 'A+'
    elif value == 'good':
        return 'A'
    elif value == 'well':
        return 'B'
    elif value == 'fair':
        return 'C'
    else:
        return None


def status(value):
    if value != 'Y':
        return 'Q'
    else:
        return 'Y'
