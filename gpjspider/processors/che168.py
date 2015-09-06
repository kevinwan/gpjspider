# -*- coding: utf-8 -*-
import re
from gpjspider.utils.constants import *
import urlparse
import requests
try:
    from gpjspider.utils.phone_parser import ConvertPhonePic2Num
except Exception, e:
    print e

base_url = 'http://www.che168.com'

def source_type(value):
    """ 对于商家车源，有：
        1、家家好车；
        2、家认证；
        3、品牌认证；
        4、保障车；
        5、普通商家车（进入店铺）
    """
    if isinstance(value, (list, tuple)):
        for val in value:
            if u'家家好车' in val:
                return SOURCE_TYPE_SELLER
            elif u'家认证' in val:
                return SOURCE_TYPE_SELLER
            elif u'品牌认证' in val:
                return SOURCE_TYPE_MANUFACTURER
            elif u'保障车' in val:
                return SOURCE_TYPE_SELLER
            elif u'进入店铺' in val:
                return SOURCE_TYPE_ODEALER
        return SOURCE_TYPE_GONGPINGJIA
    return SOURCE_TYPE_GONGPINGJIA

def is_certifield_car(value):
    if isinstance(value, (list, tuple)):
        for val in value:
            if u'家家好车' in val:
                return True
            elif u'家认证' in val:
                return True
            elif u'品牌认证' in val:
                return True
            elif u'保障车' in val:
                return True
            elif u'进入店铺' in val:
                return False
        return False
    return False

def color(value):
    """ 【图】北京二手标致408 2010款 2.0L 手动舒适版_深灰色_家家好车
        【图】北京二手本田CR-V 2010款 2.4L 自动四驱豪华版_黑色_二手车之家
        【图】郑州二手天籁 2014款 公爵 2.5L XV-VIP尊领版_银灰色_家认证
    """
    if u'色' in value:
        ret = value.split(u'_')
        for val in ret[::-1]:
            if u'色' in val:
                return val
    return ''

def city(value):
    return value.split(u'二手')[0].split(u'【图】')[-1]

def phone(value):
    if 'GetLinkPhone' in value:
        value = urlparse.urljoin(base_url, value)
    #     try:
    #         phone_info = ConvertPhonePic2Num(value).find_possible_num()
    #         value = phone_info[0]
    #         return value
    #     except Exception as e:
    #         print e
    #         return value
    # val = re.findall('\d+-\d+-\d+', value)
    # if val:
    #     return val[0]
    return value

def model_url(value):
    if re.findall('(.*pvareaid.*)', value):
        return urlparse.urljoin(base_url, value)
    return ''

def price_bn(value):
    if isinstance(value, (list, tuple)):
        specid = value[0]
        cid = value[1]

        headers = {
            "Host": "www.interface.che168.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Accept": "*/*",
            "DNT": 1,
            "Connection": "keep-alive",
        }
        url = "http://www.interface.che168.com/quoted/dealerminpricebyspec.ashx?specid=%s&cityid=%s&_callback=CarDetail.load4SPriceCallBack" % (specid, cid)
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.text
            price = re.findall('"price":"(\d+\.?\d*)"', data)
            if price:
                return price[0]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # print(doctest.testmod())
