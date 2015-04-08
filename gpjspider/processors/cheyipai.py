# -*- coding: utf-8 -*-
"""
专属车易拍的 processor
"""


def year(value):
    """
    value 示例：
    2007-1
    """
    return value.split('-')[0]


def month(value):
    """
    value 示例：
    2007-1
    """
    return value.split('-')[1]
