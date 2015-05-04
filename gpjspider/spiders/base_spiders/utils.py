# -*- coding: utf-8 -*-


def after(value, token):
    u'''
>>> after(u'保定-大众尚酷2011款2.0TSI R-line', '-')
u'\\u5927\\u4f17\\u5c1a\\u91772011\\u6b3e2.0TSI R-line'
    '''
    return token.join(value.split(token)[1:])

def before(value, token):
    u'''
>>> before(u'保定-大众尚酷2011款2.0TSI R-line', '-')
u'\\u4fdd\\u5b9a'
    '''
    return value.split(token)[0]

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
