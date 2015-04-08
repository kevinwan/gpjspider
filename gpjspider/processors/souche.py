# -*- coding: utf-8 -*-
"""
专属souche的 processor
"""


def transfer_owner(value):
    """
    """
    if isinstance(value, list):
        return len(value) - 1
    else:
        return 0


def description(value):
    """
    """
    return value.strip(' \r\n\t\b').replace(' ', '')


def imgurls(value):
    """
    """
    va = value.split(' ')
    c = []
    for v in va:
        c.append(v.split('@')[0])
    return ' '.join(c)


