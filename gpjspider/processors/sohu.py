# -*- coding: utf-8 -*-
from . import is_certified, transfer_owner as _transfer_owner
from gpjspider.utils import constants

def transfer_owner(value):
    return u'\u662f' in value and 1 or _transfer_owner(value)

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
