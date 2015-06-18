#!/usr/bin/env python
#-*-coding:utf-8-*-
import re

def color(value):
    """ 2010款 凯美瑞三厢 240G 豪华版 手自一体 黑色"""
    if isinstance(value, (list, tuple)):
        value = value[0]

    return  value.split()[-1]

def control(value):
    """ 2010款 凯美瑞三厢 240G 豪华版 手自一体 黑色"""
    if isinstance(value, (list, tuple)):
        value = value[0]

    return  value.split()[-2]

def price_bn(value):
    """ ￥24.62万（含￥1.94万购置税）"""
    if isinstance(value, (list, tuple)):
        value = value[0]
    price = re.findall('\d+\.?\d*', value)
    return str(float(price[0]) - float(price[1]))

def brand_slug(value):
    """ 成都二手丰田凯美瑞，成都二手 凯美瑞 """
    if isinstance(value, (list, tuple)):
        value = value[0]
    value = value.split()
    model = value[-1]
    brand = value[0].split(u'，')[0].split(u'二手')[-1].split(model)[0]
    return brand

def model_slug(value):
    """ 成都二手丰田凯美瑞，成都二手 凯美瑞 """
    if isinstance(value, (list, tuple)):
        value = value[0]
    return value.split()[-1]

def driving_license(value):
    if isinstance(value, (list, tuple)) and len(value) >= 1:
        value = value[0]
    if value.strip().lower() == 'yes':
        return u'是'
    return u'否'

def condition_level(value):
    """
        优+ -> Excellent -> A+
        优 -> good  -> A
        良 -> well -> B
        中 -> fair -> C
    """
    if isinstance(value, (list, tuple)):
        value = value[0]

    if value.strip().lower() == 'excellent':
        return  'A+'
    elif value.strip().lower() == 'good':
        return 'A'
    elif value.strip().lower() == 'well':
        return 'B'
    elif value.strip().lower() == 'fair':
        return 'C'
    else:
        return None

def transfer_owner(value):
    if isinstance(value, (list, tuple)):
        value = value[0]

    if  value.strip() == u'一手车':
        return 0
    else:
        return 1
