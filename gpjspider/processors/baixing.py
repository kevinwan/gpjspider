# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER, SOURCE_TYPE_GONGPINGJIA
from urllib import unquote


def phone(values):
    if isinstance(values, list):
        return values[0].replace(4 * '*', values[1])

    return None


def source_type(value):
    if value == SOURCE_TYPE_GONGPINGJIA:
        return SOURCE_TYPE_GONGPINGJIA

    return SOURCE_TYPE_ODEALER

def model_slug(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        brand = value[0].strip()
        model = value[1].strip()
        if brand in model:
            #return model.split(brand)[-1]
            return model
        return model
    return ''

def region(value):
    if 'http' in value:
        value = value.encode('ASCII')
        MAGIC = 's%26wd%3D'
        reg = value.split(MAGIC)[-1]
        if reg:
            return unquote(reg).decode('utf-8')
    else:
        return value

def car_application(value):
    if u'家用' in value:
        return u'非营运'
    return u'营运'

def invoice(value):
    if u'齐全' in value:
        return u'有'
    return u'无'

def color(value):
    if u'其它' in value:
        return ''
    if u'色' not in value:
        return value + u'色'
