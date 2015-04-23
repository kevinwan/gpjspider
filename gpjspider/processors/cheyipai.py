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


def imgurls(value):
    """
    """
    imgurls = value.split(';')
    imgurls = ['http://i.268v.com/c/{0}'.format(url) for url in imgurls]
    return ' '.join(imgurls)


def status(value):
    """
    """
    return value == 0
