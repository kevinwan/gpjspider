# -*- coding: utf-8 -*-
import re
import json
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER, SOURCE_TYPE_SELLER

import requests


def extract(value, regx, _type=None):
    if not isinstance(value, basestring):
        return value
    try:
        match = re.findall(regx, value)
        value = match[0] if match else value
        return _type(value) if _type else value
    except Exception as e:
        print e


def model_slug(value):
    return extract(value, ur'.*年款(.*)\s?\d\.\d.*')


def mile(value):
    return value + u'公里'


def region(value):
    return extract(value, ur'，(.*)') if value.find(u'，') != -1 else None


def volume(value):
    return extract(value, ur'\d\.\dL')


def phone(value):
    phone_url = u"http://www.chemao.com.cn/index.php?app=show&act=ajax_get_user_tel"
    headers = {
        'Referer': 'http://www.chemao.com.cn/',
    }

    try:
        r = requests.post(phone_url, data={'car_id': value}, headers=headers, timeout=1000)

        if r and r.status_code == 200:
            data = json.loads(r.text)
            return data['data'].replace('-', u'转')
    except Exception as e:
        print e

    return ''


def source_type(value):
    return SOURCE_TYPE_SELLER if value == 'True' else SOURCE_TYPE_ODEALER


def quality_service(value):
    normal_service = u'车辆合法，绝无火烧、水淹'
    certified_service = u'事故、水浸、火烧车7天内全款退车。1年/2万公里质保，问题车15天包退。'

    return certified_service if value == '1' else normal_service


def transfer_owner(value):
    return 0 if value == u'是' else None

