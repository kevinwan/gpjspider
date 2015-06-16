# -*- coding: utf-8 -*-
"""
专属赶集好车的 processor
"""
from decimal import Decimal
from gpjspider.utils.constants import *
import re

def transfer_owner(value):
    if isinstance(value, (list, tuple)) and len(value) > 2:
        return int(value[2])
    return int(value)

def phone(value):
    if isinstance(value, (list, tuple)):
        value = value[0]

    return value.replace(' ', '')

def source_type(value):
    if isinstance(value, (list, tuple)) and len(value) >= 1:
        value = value[0]
    if value.find(u'个人') == -1:
        return SOURCE_TYPE_ODEALER
    return SOURCE_TYPE_GONGPINGJIA

def contact(value):
    if isinstance(value, (list, tuple)):
        value = value[0]

    return value.strip().replace(' ', '')

def price_bn(val):
    if isinstance(val, (list, tuple)) and len(val) >= 1:
        return Decimal(val[0])
    return 0

def mile(val):
    if isinstance(val, (list, tuple)) and len(val) >= 1:
        val = val[0]

    return val + u'万公里'

def brand_slug(val):
    if isinstance(val, (list, tuple)) and len(val) >= 2:
        top = val[0]
        title = val[1]

        model = re.split(u'二手', top)[-1]
        title = title.split()[0]

        if model != title:
            brand = re.split(model, title)[0]
        else:
            brand = re.split('[\w\d]', title)[0]
        return brand
    return val

def model_slug(val):
    if isinstance(val, (list, tuple)) and len(val) >= 2:
        top = val[0]
        title = val[1]

        model = re.split(u'二手', top)[-1]
        title = title.split()[0]

        if model != title:
            return model
        else:
            model = re.search(r'\w+', model).group()
        return model
    return val
