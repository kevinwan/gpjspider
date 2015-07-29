# -*- coding: utf-8 -*-


def after(value, token):
    u'''
>>> after(u'保定-大众尚酷2011款2.0TSI R-line', '-')
u'\\u5927\\u4f17\\u5c1a\\u91772011\\u6b3e2.0TSI R-line'
    '''
    after_ = lambda t: t.join(value.split(t)[1:]) if t in value else value
    if isinstance(token, list):
        for tok in token:
            return after_(tok)
    return after_(token)


def before(value, token):
    u'''
>>> before(u'保定-大众尚酷2011款2.0TSI R-line', '-')
u'\\u4fdd\\u5b9a'
    '''
    before_ = lambda t: value.split(t)[0]
    if isinstance(token, list):
        for tok in token:
            value = before_(tok)
    else:
        value = before_(token)
    return value

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
