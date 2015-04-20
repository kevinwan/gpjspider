# -*- coding: utf-8 -*-
"""
专属99好车的 processor
"""


def volume(value):
    """
    例子：
    1. 大众途观 1.8T 手自一体 豪华
    """
    a = value.strip().split(' ')
    return a[1]


def transfer_owner(value):
    if u'否' in value:
        return 1
    else:
        return 0


def color(value):
    return value.split(u'，')[0]
