# -*- coding: utf-8 -*-
import re
import json
import urlparse

import requests

from gpjspider.utils.constants import SOURCE_TYPE_ODEALER, SOURCE_TYPE_SELLER


base_url = 'http://www.chemao.com.cn'


def model_url(value):
    return urlparse.urljoin(base_url, value) if value else None


def extract(value, regx, _type=None):
    if not isinstance(value, basestring):
        return value
    try:
        match = re.findall(regx, value)
        value = match[0] if match else value
        return _type(value) if _type else value
    except Exception as e:
        print e


def business_insurance(value):
    return value if value != u'过保' else u'已过期'


def model_slug(value):
    value = extract(value, ur'年款\s?(.*)\s?\d\.\d')
    value = extract(value, ur'第.+代(.*)')

    if (u'-' in value) and (u'厢' in value):
        return value.split(u'-')[0]

    return value.split(' ')[0]


def mile(value):
    return value + u'公里'


def region(value):
    return extract(value, ur'，(.*)') if value.find(u'，') != -1 else value


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
    return ' '.join(value) if isinstance(value, list) else value


def transfer_owner(value):
    return 0 if value == u'是' else None

