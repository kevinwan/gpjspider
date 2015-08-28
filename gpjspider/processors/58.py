# -*- coding: utf-8 -*-

from gpjspider.utils.constants import SOURCE_TYPE_MANUFACTURER
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA

# def city(value):
#     """
#     province=上海;city=上海;coord=121.487899,31.249162
#     """
#     try:
#         return value.split(';')[1].split('=')[1]
#     except:
#         return value

def clean_list_params(url):
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
