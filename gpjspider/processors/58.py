# -*- coding: utf-8 -*-

from gpjspider.utils.constants import SOURCE_TYPE_MANUFACTURER
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA
import re
import math
# def city(value):
#     """
#     province=上海;city=上海;coord=121.487899,31.249162
#     """
#     try:
#         return value.split(';')[1].split('=')[1]
#     except:
#         return value

def clean_list_params(url):
    return url.replace('nodownpayment=1', '')
    token = '?nodownpayment'
    return url.split(token)[0]

def clean_params(url):
    token = '&PGTID=' if 'infoid=' in url else '?'
    return url.split(token)[0]

def phone(values):
    phone_str = ''
    phone_all = ''
    value = values.split()
    for val in value:
        if len(phone_str) < 9:
            phone_str += val
        if len(phone_str) >= 9:
            phone_all += phone_str + ' '
            phone_str = ''
    return phone_all.strip()


def is_certifield_car(value):
    return any([u'7天可退' in value, u'原厂联保' in value]) if isinstance(value, str) else value


def source_type(values):
    if isinstance(values, int):
        return SOURCE_TYPE_GONGPINGJIA
    for val in values:
        if val == '1':
            return SOURCE_TYPE_MANUFACTURER
        if u'厂商认证' in val:
            return SOURCE_TYPE_MANUFACTURER  # 厂商认证
        elif val.startswith('icon_'):
            if '4S' in val:
                return SOURCE_TYPE_MANUFACTURER  # 厂商认证
            elif 'chengxincheshang' in val:
                return SOURCE_TYPE_SELLER        # 商家优质车
            else:
                return SOURCE_TYPE_ODEALER
        elif 'shop.58.com' in val:
            return SOURCE_TYPE_ODEALER
        else:
            pass
    return SOURCE_TYPE_GONGPINGJIA


def model_slug(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return value[0]
        else:
            value = ''.join([v.strip() for v in value])
            return value[value.find(u'-')+1:].strip()
    return value

def volume(value):
    if len(value) < 7:
        return value
    else:
        value = re.sub(ur'\d+(\.\d+)? *((万公里)|(公里)|里|万)','',value)
        value = re.sub(ur'\d+(\.\d+)?(Li)','',value)
        search = re.search(ur'^ *(\d+\.?\d*)[mMlLtT升]+', value) or re.search(ur' (\d+\.\d+)[mMlLtT升]+', value) or re.search(ur'(\d+\.\d+)[mMlLtT升]+', value) or re.search(ur' (\d+\.\d+) +', value) or re.search(ur'(\d+\.\d+) +', value) or re.search(ur'(\d+\.\d+)+', value) or re.search(ur' (\d+\.?\d*)[mMlLtT升] +', value)
        if search:
            val = search.group(1)
            if float(val) > 10000:
                val = float(val)
                val = math.ceil(val / 10000.0)
                return str(val / 10.0)
            elif float(val) > 100:
                val = float(val)
                val = math.ceil(val / 100.0)
                return str(val / 10.0)
            else:
                return str(float(val) / 1.0)
        return 'temp'

def control(value):
    contr = re.search(u'双离合|无级变?速?', value)
    if contr:
        return u'自动'
    else:
        return value
