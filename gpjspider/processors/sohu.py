# -*- coding: utf-8 -*-
from . import is_certified, transfer_owner as _transfer_owner
from gpjspider.utils.constants import *
import re

def transfer_owner(value):
    return u'\u662f' in value and 1 or _transfer_owner(value)

def source_type(value):
    if isinstance(value, dict):
        st = value.get('_source_type')
        company = value.get('company_name')
        if st:
            if u'品牌认证' in st:
                return SOURCE_TYPE_MANUFACTURER
            elif u'尊沃' in st:
                return SOURCE_TYPE_MANUFACTURER
            elif u'认证' in st:
                return SOURCE_TYPE_SELLER
            else:
                return SOURCE_TYPE_ODEALER
        elif company:
            return SOURCE_TYPE_ODEALER
        else:
            return SOURCE_TYPE_GONGPINGJIA

def brand_slug(value):
    if value.count(u'二手') == 5:
        value = value.replace(u'，', '').split(u'二手')
        return value[2].strip()
    return ''

def model_slug(value):
    if value.count(u'二手') == 5:
        value = value.replace(u'，', '').split(u'二手')
        brand = value[2].strip()
        model = value[3].strip().split()[0].split(brand)[-1]
        return model
    return ''

def status(value):
    if value != 'Y':
        return 'Q'
    else:
        return 'Y'

def is_certifield_car(value):
    if isinstance(value, dict):
        item = value
        st = item.get('_source_type', None)
        if st:
            if u'认证' in st:
                return True
            elif st == SOURCE_TYPE_MANUFACTURER:
                return True
            else:
                return False
        else:
            return False

def company_name(value):
    if u'联系电话' in value:
        return ''
    return value

def region(value):
    last = value[-1].strip()
    if u'--' in last:
        return ''
    return last

def volume(value):
    val = re.match(u'(\d)[LT]', value)
    if val:
        return val.group(1) + '.0'
    else:
        return value

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
