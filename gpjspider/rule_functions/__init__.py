# -*- coding: utf-8 -*-
"""
rule_function的定义

规则：
 'function':{
    'name': 'xxxxx',
    'args': (a1, a2),
    'kwargs': {'k1': 'xxx', ... }
 },

函数名的命名惯例：
域名_字段名(response, spider, *args, **kwargs)


def rule_function(response, spider, *args, **kwargs):
    return anything

"""


# def haoche51_city(response, spider, *args, **kwargs):
#     """
#     """


def cheyipai_url(response, spider, *args, **kwargs):
    """
    车易拍的 url 规则函数
    """
    s_idx = response.url.find('id%22%3A%22')
    s_idx += len('id%22%3A%22')
    e_idx = response.url.find('%22%7D', s_idx)
    id = response.url[s_idx:e_idx]
    return 'http://c.cheyipai.com/car_detail.jsp?goodsid={0}'.format(id)
