# -*- coding: utf-8 -*-
# from gpjspider.processors.common import is_certified
from . import is_certified
from gpjspider.utils import constants


def source_type(value):
    u'''
>>> source_type('http://dealer.che168.com/login.html?backurl=http://www.che168.com/personal/4323708.html#pvareaid=100522#pos=2')
4

# >>> source_type(u'http://dealer.che168.com/login.html?backurl=http://www.che168.com/personal/4323708.html#pvareaid=100522#pos=2 质保')
# 4
# >>> source_type(u'http://dealer.che168.com/login.html?backurl=http://www.che168.com/personal/4323708.html#pvareaid=100522#pos=2 质保')
# 4
# >>> source_type(u'http://dealer.che168.com/login.html?backurl=http://www.che168.com/dealer/106732/4808187.html#pvareaid=100522#pos=2 质保 品牌认证')
# 4
>>> source_type('/dealer/106732/4808187.html#pvareaid=100520#pos=2')
5
    '''
    # print value
    st = None 	# constants.SOURCE_TYPE_GONGPINGJIA
    if '/personal/' in value or '/dealer/0/' in value:
        st = constants.SOURCE_TYPE_GONGPINGJIA
    elif '/dealer/' in value:
        st = constants.SOURCE_TYPE_ODEALER
        if is_certified(value):
            st = constants.SOURCE_TYPE_SELLER
            if u'品牌认证' in value:
                st = constants.SOURCE_TYPE_MANUFACTURER
    return st

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # print(doctest.testmod())
