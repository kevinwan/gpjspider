# -*- coding: utf-8 -*-
"""
专属99好车的 processor
"""
import requests
import re

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

def phone(value):
    phone_url = "http://www.99haoche.com/shop/get400Phone.do?carId={0}".format(value)
    try:
        r = requests.get(phone_url, timeout=10)
        if r and r.status_code == 200:
            data = r.text.strip()
            if re.match('\d{10}', data) or re.match('\d{3}-\d{3}-\d{4}', data):
                return data
    except Exception as e:
        print e
    return ''

def condition_level(value):
    if not isinstance(value, list):
        return ''
    url = "http://www.99haoche.com/ajax/getCarInspectionReport.do?carId={0}".format(value[1])
    headers = {
        'Host': 'www.99haoche.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
        'Connection': 'keep-alive',
    }

    cookies = {
        'JSESSIONID': 'AF228F614289D944455248AAD376AB4B',
    }

    level = ''

    try:
        s = requests.Session()
        s.headers.update(headers)

        r = s.request('GET', url, cookies=cookies)

        if r and r.status_code == 200 and len(r.content) > 0:
            jdata = r.json()
            jdata = jdata.get('generalCheck', {})
            if jdata:
                level = jdata.get('level', '')
    except Exception as e:
        print e

    return level
