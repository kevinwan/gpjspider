# -*- coding: utf-8 -*-
from . import is_certified
from gpjspider.utils.constants import *
import pdb
import re


def phone(value):
    '''
>>> phone('http://cache.taoche.com/buycar/gettel.ashx?u=5730860&t=ciggmcamamm')
4008138214
    '''
    return value

#def source_type(value):
    #u'''
#>>> source_type('http://dealer.che168.com/login.html?backurl=http://www.che168.com/personal/4323708.html#pvareaid=100522#pos=2')
#4

## >>> source_type(u'http://dealer.che168.com/login.html?backurl=http://www.che168.com/personal/4323708.html#pvareaid=100522#pos=2 质保')
## 4
## >>> source_type(u'http://dealer.che168.com/login.html?backurl=http://www.che168.com/personal/4323708.html#pvareaid=100522#pos=2 质保')
## 4
## >>> source_type(u'http://dealer.che168.com/login.html?backurl=http://www.che168.com/dealer/106732/4808187.html#pvareaid=100522#pos=2 质保 品牌认证')
## 4
#>>> source_type('/dealer/106732/4808187.html#pvareaid=100520#pos=2')
#5
    #'''
    ## print value
    #st = None 	# constants.SOURCE_TYPE_GONGPINGJIA
    ## pdb.set_trace()
    #try:
        #int(value)
        #st = constants.SOURCE_TYPE_GONGPINGJIA
    #except:
        #if 'Dealer' in value:
            #st = constants.SOURCE_TYPE_ODEALER
            #if is_certified(value):
                #st = constants.SOURCE_TYPE_SELLER
                #if u'品牌认证' in value:
                    #st = constants.SOURCE_TYPE_MANUFACTURER
    #return st

def source_type(value):
    """ 数据中包含了图片，就是 品牌二手车、仅有链接，就是商家， 否则是个人 """
    if isinstance(value, (list, tuple)):
        for val in value:
            if 'img' in val:
                return SOURCE_TYPE_MANUFACTURER
        return SOURCE_TYPE_ODEALER
    return SOURCE_TYPE_GONGPINGJIA

def description(value):
    if isinstance(value, (list, tuple)):
        for val in value[:]:
            if u'易车二手车' in val:
                value.remove(val)
        return ' '.join([val.strip() for val in value])
    return value

def mile(value):
    val = re.search('\d+\.?\d*', value)
    if val:
        return val.group() + u'万公里'
    return 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # print(doctest.testmod())
