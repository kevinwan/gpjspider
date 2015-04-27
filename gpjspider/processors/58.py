# -*- coding: utf-8 -*-

from gpjspider.utils.constants import SOURCE_TYPE_MANUFACTURER
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA


def city(value):
    """
    province=上海;city=上海;coord=121.487899,31.249162
    """
    try:
        return value.split(';')[1].split('=')[1]
    except:
        return value


def phone(values):
    """
    """
    vs = []
    for value in values:
        v = value.strip()
        try:
            long(v)
        except:
            continue
        else:
            vs.append(v)
    return ''.join(vs)


def is_certifield_car(value):
    """
    """
    return any([
        u'7天可退' in value,
        u'原厂联保' in value,
    ])


def source_type(values):
    """
    """
    for value in values:
        if value == '1':
            return SOURCE_TYPE_MANUFACTURER
        if 'http://shop.58.com' in value:
            return SOURCE_TYPE_ODEALER
    _v = u' '.join(values)
    if any([u'7天可退' in _v, u'原厂联保' in _v]):
        return SOURCE_TYPE_SELLER
    # 个人车
    return SOURCE_TYPE_GONGPINGJIA
