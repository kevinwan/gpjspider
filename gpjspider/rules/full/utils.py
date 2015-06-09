# -*- coding: utf-8 -*-
try:
    from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA
except ImportError:
    pass

attr = lambda x, e: '//%s/@%s' % (x, e)
url = lambda x: attr(x + '/a[@href]', 'href')
img = lambda x: attr(x + '/img[@src]', 'src')
text = lambda x: '//%s/text()' % x
value = lambda x: '//%s/@value' % x
string = lambda x: text(x + '/')
index = lambda x, i: '(%s)[%s]' % (x, i)
first = lambda x: index(x, '1')
last = lambda x: index(x, 'last()')
after = lambda x, e: x + '/following-sibling::' + e
exists = lambda x: 'boolean(//%s)' % x


# id_ = lambda x: '*[@id="%s"]' % x
def id_(_id, subfix=''):
    return '*[@id="%s"]%s' % (_id, subfix)
hidden = lambda x: value(id_(x))

# from urllib import urlparse
# TODO: use urlparse
def full_url(base_url):
    return base_url + '{0}'


def has(value, subfix='', prefix='*', get_text=True):
    node = u'%s[contains(text(), "%s")]%s' % (prefix, value, subfix)
    return text(node) if not node.endswith('()') else ('//' + node)


def after_has(value, node='*', *args, **kwargs):
    return has(value, '/following-sibling::' + node, *args, **kwargs)


def has_attr(attr, value, subfix=''):
    return '*[contains(@%s,"%s")]%s' % (attr, value, subfix)

def has_cls(cls, subfix=''):
    return has_attr('class', cls, subfix)

def has_id(cls, subfix=''):
    return has_attr('id', cls, subfix)

def with_cls(cls, subfix='', prefix=''):
    return '%s*[@class="%s"]%s' % (prefix, cls, subfix)
cls = with_cls

def fmt_urls(rule, base_url):
    for k, v in rule.items():
        if v.get('format') is True:
            v['format'] = full_url(base_url)


def fmt_rule_urls(rule):
    base_url = rule.get('base_url')
    if base_url:
        fmt_urls(rule['parse'], base_url)
        if 'parse_list' in rule:
            fmt_urls(rule['parse_list'], base_url)
        fmt_urls(rule['parse_detail']['item']['fields'], base_url)


def test():
    u'''
>>> has(u't')
u'//*[contains(text(), "t")]/text()'
>>> after_has(u't', 'span[1]//text()')
u'//*[contains(text(), "t")]/following-sibling::span[1]//text()'
>>> exists(id_('icon_chengxincheshang'))
'boolean(//*[@id="icon_chengxincheshang"])'
>>> attr(has_id('icon_'), 'id')
'//*[contains(@id,"icon_")]/@id'
>>> has('test', '/../em', 'li/span')
u'//li/span[contains(text(), "test")]/../em/text()'
>>> after_has('test', 'td', 'td')
u'//td[contains(text(), "test")]/following-sibling::td/text()'
>>> img(cls('day-pic'))
'//*[@class="day-pic"]/img[@src]/@src'
    '''

def main():
    import doctest
    print doctest.testmod()

if __name__ == '__main__':
    main()