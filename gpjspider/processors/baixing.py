# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER, SOURCE_TYPE_GONGPINGJIA


def phone(values):
    if isinstance(values, list):
        return values[0].replace(4 * '*', values[1])

    return None


def source_type(value):
    if value != 'None':
        return SOURCE_TYPE_GONGPINGJIA

    return SOURCE_TYPE_ODEALER
