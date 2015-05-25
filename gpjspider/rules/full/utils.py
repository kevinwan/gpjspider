# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA

attr = lambda x, e: '//%s/@%s' % (x, e)
url = lambda x: attr(x + '/a[@href]', 'href')
text = lambda x: '//%s/text()' % x
value = lambda x: '//%s/@value' % x
string = lambda x: text(x + '/')
hidden = lambda x: value('*[@id="%s"]' % x)
index = lambda x, i: '(%s)[%s]' % (x, i)
first = lambda x: index(x, '1')
last = lambda x: index(x, 'last()')
after = lambda x, e: x + '/following-sibling::' + e
# from urllib import urlparse


def to_url(base_url):
    return base_url + '{0}'


def has(value, style='', prefix='', get_text=True):
    node = u'%s*[contains(text(), "%s")]%s' % (prefix, value, style)
    return text(node) if not node.endswith('()') else ('//' + node)


def after_has(value, node='*', *args, **kwargs):
    return has(value, '/following-sibling::' + node, *args, **kwargs)


def has_cls(cls, subfix=''):
    return '*[contains(@class,"%s")]%s' % (cls, subfix)


def with_cls(cls, subfix='', prefix=''):
    return '%s*[@class="%s"]%s' % (prefix, cls, subfix)


def fmt_urls(rule, base_url):
    for k, v in rule.items():
        # if 'url' in k and v.get('format') == True:
        if v.get('format') == True:
            v['format'] = to_url(base_url)


def fmt_rule_urls(rule):
    base_url = rule.get('base_url')
    if base_url:
        fmt_urls(rule['parse'], base_url)
        fmt_urls(rule['parse_detail']['item']['fields'], base_url)
