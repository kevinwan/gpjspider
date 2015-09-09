# -*- coding: utf-8 -*-
"""
专属renreche的 processor
"""


def city_slug(city_url):
    """
    """
    return city_url.strip('/')


def region(region_str):
    """
    车主：张先生 | 公司职员
地址：二七路轻轨站附近
    """
    return region_str.split(u'：')[-1]


def cond_level(value):
    """
    1. 极品车况：
    2. 优秀车况
    """
    if u'极品车况' in value:
        return u'极品'
    elif u'优秀车况' in value:
        return u'优秀'
    else:
        return ''


BRANDS = {}


def setup_brand(item):
    global BRANDS
    BRANDS[item['slug']] = item['name']


def get_model_parent(value):
    global BRANDS
    return BRANDS[value]
