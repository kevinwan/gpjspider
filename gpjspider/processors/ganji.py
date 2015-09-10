# -*- coding: utf-8 -*-
"""
专属赶集好车的 processor
"""
from decimal import Decimal
from gpjspider.utils.constants import *
from datetime import datetime
import re


def transfer_owner(value):
    if isinstance(value, (list, tuple)) and len(value) > 2:
        return int(value[2])
    if isinstance(value, (list, tuple)):
        if u'次' in value[0]:
            return int(value[0].strip(u'次'))
    return int(value)


def phone(value):
    return value.replace(' ', '')


def source_type(value):
    if isinstance(value, (list, tuple)) and len(value) >= 1:
        value = value[0]
    if value.find(u'个人') == -1:
        return SOURCE_TYPE_ODEALER
    return SOURCE_TYPE_GONGPINGJIA


def contact(value):
    return value.strip().replace(' ', '')


def mile(val):
    return val + u'万公里'


def brand_slug(val):
    if isinstance(val, (list, tuple)):
        if len(val) >= 2:
            top = val[0]
            title = val[1]

            model = re.split(u'二手', top)[-1]
            title = title.split()[0]

            if model != title:
                brand = re.split(model, title)[0]
            else:
                brand = re.split('[\w\d]', title)[0]
            return brand
        else:
            return val[0]
    return val


def model_slug(val):
    # import ipdb;ipdb.set_trace()
    if isinstance(val, (list, tuple)):
        if len(val) >= 2:
            top = val[0]
            title = val[1]

            model = re.split(u'二手', top)[-1]
            title = title.split()[0]

            if model != title:
                return model
            else:
                model = re.search(r'\w+', model)
                if model:
                    return model.group()
                else:
                    return ''
        else:
            return val[0]
    return val


def volume(val):
    vol = re.match(u'(\d+)[LT]', val)
    if vol:
        return vol.group(1) + '.0'
    else:
        return val


def time(value):
    try:
        now_time = datetime.now()
        fmt_time = str(now_time.year) + '-' + value
        fmt_time = fmt_time.split(' ')[0]
        pub_time = datetime.strptime(fmt_time, "%Y-%m-%d")
        if pub_time > now_time:
            return str(now_time.year - 1) + '-' + value
        else:
            return value
    except:
        return value
