# -*- coding: utf-8 -*-
from . import is_certified
from gpjspider.utils import constants


def source_type(value):
    u'''
    '''
    st = constants.SOURCE_TYPE_GONGPINGJIA
    if u'商家' in value:
        st = constants.SOURCE_TYPE_ODEALER
        if is_certified(value):
            st = constants.SOURCE_TYPE_SELLER
        if u'品牌认证' in value:
            st = constants.SOURCE_TYPE_MANUFACTURER
    return st

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
