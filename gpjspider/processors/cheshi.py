#!/usr/bin/env python
#-*-coding:utf-8-*-
import re
from gpjspider.utils.constants import *

def color(value):
    """
        【出售广东二手黑色大众帕萨特2001款 帕萨特 旅行车 1.8T 自动(进口) 买费用都值啦】_14年行驶17.00万公里-网上车市
        【出售湖北二手黑2012款&nbsp;30 FSI CVT&nbsp;豪华型】_2年行驶4.00万公里-网上车市
        【出售北京二手深灰色2012款&nbsp;E200L 1.8T&nbsp;CGI优雅型】_3年行驶7.90万公里-网上车市
    """
    if u'色' in value:
        ret = re.findall(u'二手(\S+色)', value)
        if ret:
            return ret[0]
        else:
            return ''
    else:
        ret = re.findall(u'二手(\S{1,2})\d*', value)
        if ret and u'其他' not in ret[0]:
            if re.search('\d+', ret[0]):
                return ret[0][:-1]
            else:
                return ret[0]
        else:
            return ''

def brand_or_model(value):
    if u'车' in value:
        return ''
    if u'二手' in value:
        if re.search(u'二手(.*)', value):
            return re.search(u'二手(.*)', value).group(1)
        return ''
    return ''

def source_type(value):
    if u'个人' in value:
        return SOURCE_TYPE_GONGPINGJIA
    elif u'4' in value:
        return SOURCE_TYPE_SELLER
    elif u'商家' in value:
        return SOURCE_TYPE_ODEALER

def model_url(value):
    """ /zhengzhou/chevrolet/73/ """
    if value.count('/') == 4:
        return value
    else:
        return ''


