# -*- coding: utf-8 -*-
attr = lambda x, e: '//%s/@%s' % (x, e)
url = lambda x: attr(x + '/a[@href]', 'href')
text = lambda x: '//%s/text()' % x
string = lambda x: text(x + '/')
# from urllib import urlparse


def to_url(base_url):
    return base_url + '{0}'


def has(value, style='', prefix=''):
    return text(u'%s*[contains(text(), "%s")]%s' % (prefix, value, style))


def after_has(value, node='*'):
    return has(value, '/following-sibling::' + node)


def has_cls(cls, subfix=''):
    return '*[contains(@class,"%s")]%s' % (cls, subfix)


def with_cls(cls, subfix=''):
    return '*[@class="%s"]%s' % (cls, subfix)
