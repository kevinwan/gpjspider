# -*- coding: utf-8 -*-
"""
专属souche的 processor
"""
import re
import requests


def transfer_owner(value):
    #if isinstance(value, list):
        #return len(value) - 1
    #else:
        #return 0
    carid = value.split('=')[-1]
    url = "http://www.souche.com/pages/carDetailTransferAction/transfer.json?carId={0}".format(carid)
    num = 0

    try:
        r = requests.get(url, timeout=10)
        if r and r.status_code == 200 and len(r.content) > 0:
            jdata = r.json()
            num = jdata.get('num', 0)
    except Exception as e:
        print e

    return num

def imgurls(value):
    token = '?' in value and '?' or '@' in value and '@' or None
    if token:
        value = ' '.join([v.split(token)[0] for v in value.split(' ')])
    return value

def condition_level(value):
    """ 质检A
        质检B+
        质检C-
    """
    if isinstance(value, list):
        value = value[0]
    return re.search('\w+[+-]?', value).group()

