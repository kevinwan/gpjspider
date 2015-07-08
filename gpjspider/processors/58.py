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


# def phone(values):
#     vs = []
#     for value in values:
#         v = value.strip()
#         try:
#             long(v)
#         except:
#             continue
#         else:
#             vs.append(v)
#     return ''.join(vs)


def is_certifield_car(value):
    return any([u'7天可退' in value, u'原厂联保' in value]) if isinstance(value, str) else value


def source_type(values):
    # print values
    st = SOURCE_TYPE_GONGPINGJIA
    for value in values:
        if value == '1':
            st = SOURCE_TYPE_MANUFACTURER
            break
        if value.startswith('icon_'):
            st = SOURCE_TYPE_SELLER
            break
            if 'renzheng' in value:
                return SOURCE_TYPE_MANUFACTURER
            elif 'chengxin' in value or '4S' in value:
                return SOURCE_TYPE_SELLER
        elif 'http://shop.58.com' in value:
            st = SOURCE_TYPE_ODEALER
            break
    # _v = u' '.join(values)
    # if is_certifield_car(_v):
    #     st = SOURCE_TYPE_SELLER
    return st

def model_slug(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return value[0]
        else:
            value = ''.join([v.strip() for v in value])
            return value[value.find(u'-')+1: ].strip()
    return value
