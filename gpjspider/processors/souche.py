# -*- coding: utf-8 -*-
"""
专属souche的 processor
"""


def transfer_owner(value):
    if isinstance(value, list):
        return len(value) - 1
    else:
        return 0

def imgurls(value):
    token = '?' in value and '?' or '@' in value and '@' or None
    if token:
        value = ' '.join([v.split(token)[0] for v in value.split(' ')])
    return value
