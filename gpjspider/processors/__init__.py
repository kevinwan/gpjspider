# -*- coding: utf-8 -*-
"""
自定义 processor
在字段规则定义中，processor路径是基于 gpjspider.processors的，
如 cheyipai.year 表示 cheyipai 模块的 year函数

processor暂不支持除 value 之外的参数
"""
from decimal import Decimal
import re
import pdb
# pdb.set_trace()
from datetime import datetime, timedelta
from dateutil.parser import parse
from exceptions import TypeError

reg_blank_split = re.compile(r'\s+')


def strip(value):
    '''
    如果是字符串，去除空格 \r  \n \t
    如果不是，原样返回
    '''
    if not isinstance(value, basestring):
        return value
    value = value.replace(u'\xa0', u'')
    value = value.replace(u'\xb7', u'')
    return value.strip('\t\r\n\b ')


def first(value):
    if isinstance(value, (list, tuple)):
        return strip(value[0])
    else:
        return value


def last(value):
    if isinstance(value, (list, tuple)):
        return strip(value[-1])
    else:
        return value


def join(values, token=' '):
    '''
    todo:  暂时用空格 join
    '''
    value = [strip(v) for v in values]
    if isinstance(value, (list, tuple)):
        return token.join(value)
    else:
        return value


def comma_join(values):
    return join(values, ', ')


def concat(values):
    value = [strip(v) for v in values]
    if isinstance(value, (list, tuple)):
        return ''.join(value)
    else:
        return value


def quality_service(values):
    u'''
>>> quality_service(u'质保到期： 已过期,延长质保： ,24,个月/,9.9,万公里&nbsp;(自您购车日起算)'.split(','))
u'\\u8d28\\u4fdd\\u5230\\u671f\\uff1a\\u5df2\\u8fc7\\u671f, \\u5ef6\\u957f\\u8d28\\u4fdd\\uff1a24\\u4e2a\\u6708/9.9\\u4e07\\u516c\\u91cc&nbsp;(\\u81ea\\u60a8\\u8d2d\\u8f66\\u65e5\\u8d77\\u7b97)'
>>> quality_service(u'质保到期： test,原厂延保： ,24,个月/,9.9,万公里&nbsp;(自您购车日起算)'.split(','))
u'\\u8d28\\u4fdd\\u5230\\u671f\\uff1atest, \\u539f\\u5382\\u5ef6\\u4fdd\\uff1a24\\u4e2a\\u6708/9.9\\u4e07\\u516c\\u91cc&nbsp;(\\u81ea\\u60a8\\u8d2d\\u8f66\\u65e5\\u8d77\\u7b97)'
    '''
    value = isinstance(values, (list, tuple)) and concat(values).replace(' ', '') or values
    match = re.findall(ur'(.{3}保)：', value)
    # match = re.findall(ur'(延长质保|原厂延保)：', value)
    # match = re.findall(ur'([原厂]{,2}延.{,2}保)：', value)
    if match:
        qs = match[0]
        value = value.replace(qs, ', ' + qs)
    return value


def strip_html(value):
    assert isinstance(value, basestring)
    return value.strip('<br>').strip('<br/>').strip('<br />')


def gpjint(value):
    return convert(value, int)


def gpjfloat(value):
    return convert(value, float)


def decimal(value):
    return convert(value, Decimal)


def convert(value, _type, default=None):
    try:
        if isinstance(value, basestring):
            value = value.strip()
        if not isinstance(value, _type):
            value = _type(value)
    except:
        value = value or default
    return value


def volume(value):
    u'''
>>> volume(u'大众途观 1.8T 手自一体 豪华')
1.8
    '''
    a = re.compile(r'(\d\.\d)').findall(value)
    return a and gpjfloat(a[0]) or None


def brand_slug(value):
    u'''
>>> brand_slug(u'test  唯雅诺')
u'test'
>>> brand_slug(u'test >')
u'test'
>>> brand_slug(u'test-菲翔2012款')
u'test'
>>> brand_slug(u'二手test')
u'test'
    '''
    a = value.strip('> ').lstrip(u'二手')
    a = reg_blank_split.split(a)
    if '-' in a[0]:
        a = a[0].split('-')
    return a[0].strip()


def model_slug(value):
    u'''
>>> model_slug(u'1  test')
u'test'
>>> model_slug(u'test >')
u'test'
>>> model_slug(u'a-test')
u'test'
>>> model_slug(u'二手test')
u'test'
    '''
    value = value.strip('> ').lstrip(u'二手')
    if ' ' in value:
        a = reg_blank_split.split(value)
        return a[1]
    elif '-' in value:
        a = value.split('-')
        return a[1]
    else:
        return value


def city(value):
    u'''
>>> city(u'河北 石家庄')
u'\\u77f3\\u5bb6\\u5e84'
    '''
    if ' ' in value:
        value = value.split()[-1]
    else:
        value = value.strip(u'二手车城市>')
    return value


def strip_url(url_with_query):
    '''
    去除 URL 里的 querystring
    '''
    if '?' in url_with_query:
        return url_with_query.split('?')[0]
    else:
        return url_with_query


def strip_imgurls(urls_with_query):
    '''
    专门用于strip 掉 imgurl 的 url 中包含的 querystring
    '''
    urls_with_query = urls_with_query.split()
    new_urls = []
    for url in urls_with_query:
        new_urls.append(strip_url(url))
    return ' '.join(new_urls)


def status(value):
    if value == '1':
        return True
    elif value == '0':
        return False
    return bool(value)


def price(value):
    u'''
>>> price(u'￥128.00万')
Decimal('128.00')
>>> price(u'21.68万')
Decimal('21.68')
>>> price(u'12.36')
Decimal('12.36')
>>> price(u'¥ 6.5')
Decimal('6.5')
>>> price(u'¥ 65')
Decimal('65')
    '''
    v = extract(value, ur'[^\d]*(\d*\.?\d{1,2})万', decimal)
    if isinstance(v, basestring) and value and not u'万' in value:
        v = extract(value, ur'[^\d]*(\d*\.?\d{1,2})', decimal)
    if isinstance(v, Decimal) and v > 10000:
        v /= 10000
    return v


def price_bn(value):
    u'''
>>> price_bn(u'新车价：29.88万+2.56万（购置税）')
Decimal('29.88')
>>> price_bn(u'新车：31.80万 + 2.72万购置税')
Decimal('31.80')
>>> price_bn(u'(裸车价44.95万元+购置税3.84万元)')
Decimal('44.95')
    '''
    v = extract(value, ur'[新车价]{2,}[^\d]{,2}(\d*\.?\d{1,2})万', decimal)
    if isinstance(v, basestring) and value and not u'万' in value:
        v = extract(value, ur'[新车价]{2,}[^\d]{,2}(\d*\.?\d{1,2})', decimal)
    if isinstance(v, Decimal) and v > 10000:
        v /= 10000
    return v


def mile(value):
    u'''
>>> mile(u'0.1万公里')
Decimal('0.1')
>>> mile(u'7万公里')
Decimal('7')
>>> mile(u'55')
Decimal('0.0055')
>>> mile(u'600公里')
Decimal('0.06')
>>> mile(u'600')
Decimal('0.06')
    '''
    v = extract(value, ur'[^\d]*(\d*\.?\d{1,2})万公里', decimal)
    if isinstance(v, Decimal) and v > 100 or value and not u'万' in value:
        v = extract(value, ur'(\d+)公里', decimal) / 10000
    return v


def year(value):
    u'''
>>> year('2007-1')
2007
>>> year(u'2014年09月')
2014
    '''
    return extract(value, ur'(\d{4}).\d{1,2}', gpjint)


def month(value):
    u'''
>>> month('2007-1')
1
>>> month(u'2014年09月')
9
>>> month(u'2012年3月')
3
    '''
    return extract(value, ur'\d{4}.(\d{1,2})', gpjint)


def get_overdue_date():
    date = gpjtime_bytimedelta(u'1周前')
    return u'-'.join([str(e) for e in [date.year, date.month, 1]])


def year_month(value):
    u'''
>>> year_month(u'保险到期： 2014-7')
u'2014-7-1'
>>> year_month(u'已过期')
u'2015-4-1'
    '''
    regx = re.compile(ur'(\d{4}).(\d{1,2})')
    a = regx.findall(value)
    if a:
        return u'-'.join(a[0]) + u'-1'
    else:
        return u'已过期' in value and get_overdue_date() or ''

mandatory_insurance = year_month
business_insurance = year_month
examine_insurance = year_month


def str_to_unicode(value, encoding):
    return unicode(value, encoding) if isinstance(value, str) else value


def gpj_now():
    return datetime.now()


def gpjtime(time, to_str=True):
    u"""
>>> isinstance(gpjtime(u'1天前', False), datetime)
True
>>> isinstance(gpjtime(u'昨天', False), datetime)
True
>>> gpjtime('test')
>>> gpjtime(u'2012-3-10 14小时9分3')
'2012-03-10 14:09:03'
>>> gpjtime(u'2012年3月10 14:9:3')
'2012-03-10 14:09:03'
>>> gpjtime(u'2012年3月10 14小时9分3')
'2012-03-10 14:09:03'
    """
    if u'已过期' in time:
        return None
    elif u'昨天' in time:
        time = u'1天前'
    elif u'前天' in time:
        time = u'2天前'
    t = gpjtime_bytimedelta(time)
    time = t if isinstance(t, datetime) else gpjtime_byfmt(t)
    return to_str and time and str(time)[:19] or time


def gpjtime_bytimedelta(time, strick=False, encoding='utf-8'):
    u"""
>>> isinstance(gpjtime_bytimedelta(u'0秒前'), datetime)
True
>>> isinstance(gpjtime_bytimedelta(u'1秒前'), datetime)
True
>>> isinstance(gpjtime_bytimedelta(u'2小时前'), datetime)
True
>>> isinstance(gpjtime_bytimedelta(u'1天前'), datetime)
True
>>> isinstance(gpjtime_bytimedelta(u'1周前'), datetime)
True
>>> isinstance(gpjtime_bytimedelta(u'1星期前'), datetime)
True
>>> isinstance(gpjtime_bytimedelta(u'1月前'), datetime)
False
>>> isinstance(gpjtime_bytimedelta(u'1年前'), datetime)
False
    """
    time = str_to_unicode(time, encoding)
    tag = [(u'秒前', 'S', 1), (u'分钟前', 'S', 60), (u'小时前', 'S', 3600),
           (u'天前', 'D', 1),  (u'周前', 'D', 7), (u'星期前', 'D', 7), ]
    delta = None
    for p, u, s in tag:
        if p in time:
            t = time[:time.find(p)]
            delta = timedelta(
                seconds=int(t) * s) if u == 'S' else timedelta(days=int(t) * s)
            break
    if strick:
        if not delta:
            raise TypeError(u'time {0} not matched format n<U> 前'.format(time))
        else:
            return gpj_now() - delta
    else:
        return gpj_now() - delta if delta is not None else time


def gpjtime_byfmt(time, encoding='utf-8'):
    u"""
>>> gpjtime_byfmt(u'2012年3月10')
datetime.datetime(2012, 3, 10, 0, 0)
>>> gpjtime_byfmt(u'2014年01月09日')
datetime.datetime(2014, 1, 9, 0, 0)
>>> gpjtime_byfmt('2012年3月10')
datetime.datetime(2012, 3, 10, 0, 0)
>>> gpjtime_byfmt('2012年3月10 12:49:3')
datetime.datetime(2012, 3, 10, 12, 49, 3)
>>> gpjtime_byfmt('2012年3月10日 12:49:3')
datetime.datetime(2012, 3, 10, 12, 49, 3)
>>> gpjtime_byfmt('3月10日 12:49:3')
datetime.datetime(2015, 3, 10, 12, 49, 3)
>>> gpjtime_byfmt('2012年3月10 14小时9分3')
datetime.datetime(2012, 3, 10, 14, 9, 3)

# >>> gpjtime_byfmt('12-3')
# datetime.datetime(2014, 12, 3, 0, 0)
>>> a = gpjtime_byfmt(u'2012年3月')
>>> a.month
3
>>> a = gpjtime_byfmt(u'2012年4月')
>>> a.month
4
>>> a.day
1
    """
    time = str_to_unicode(time, encoding)
    dunit = (u'年', u'月', u'日', u'号')
    tunit = (u'小时', u'分钟', u'分', u'秒')

    if u'日' in time:
        time = time.replace(u'日', '')
    if u'号' in time:
        time = time.replace(u'号', '')
    for d in dunit:
        if d in time:
            time = time.replace(d, '-')
    for t in tunit:
        if t in time:
            time = time.replace(t, ':')
    time = time.strip('-')
    time = time.strip(':')
    dft_tm = datetime(gpj_now().year, gpj_now().month, 1)
    try:
        return parse(time, default=dft_tm)
    except:
        return


def gpjtime_strict(time, range=10):
    u"""
    the time get must older than now

    @param range: range minutes

    >>> gpjtime_strict('12-3')
    datetime.datetime(2014, 12, 3, 0, 0)
    >>> gpjtime_strict(u'2014-03-22 07:59:40')
    datetime.datetime(2014, 3, 22, 7, 59, 40)
    >>> isinstance(gpjtime_strict(u'3天前'), datetime)
    True
    """
    t = gpjtime(time, False)
    return t - timedelta(days=365) if t > gpj_now() + timedelta(seconds=int(range) * 60) else t


def clean_anchor(value):
    '''
>>> clean_anchor('http://www.che168.com/dealer/85459/4807604.html#pvareaid=100519')
'http://www.che168.com/dealer/85459/4807604.html'
>>> clean_anchor('/autonomous/4650620.html#pvareaid=100522#pos=11')
'/autonomous/4650620.html'
    '''
    return extract(value, '([^#]+)#?.*')


def after_space(value):
    u'''
>>> after_space(u'维修保养： 定期4S保养')
u'\\u5b9a\\u671f4S\\u4fdd\\u517b'
    '''
    return value.split()[1]


def after_colon(value):
    u'''
>>> after_colon(u'维修保养： 定期4S保养')
u'\\u5b9a\\u671f4S\\u4fdd\\u517b'
    '''
    regx = ur'[:：]\s*(.*)$'
    return extract(value, regx)


def extract(value, regx, _type=None):
    if not isinstance(value, basestring):
        return value
    try:
        match = re.findall(regx, value)
        value = match[0] if match else value
        return _type(value) if _type else value
    except Exception as e:
        print e
        # print value, regx


def dmodel(value):
    u'''
>>> dmodel(u'大众迈腾2009款1.8TSI 手动 舒适型')
u'2009\\u6b3e1.8TSI \\u624b\\u52a8 \\u8212\\u9002\\u578b'
>>> dmodel(u'大众迈腾09款1.8TSI 手动 舒适型')
u'09\\u6b3e1.8TSI \\u624b\\u52a8 \\u8212\\u9002\\u578b'
    '''
    return extract(value, u'(\d{2}款.+|\d{4}款.+)$')


def is_certified(value):
    u'''
>>> is_certified(u'原厂质保')
True
    '''
    # pdb.set_trace()
    return value == '1' or u'质保' in value or u'保障' in value or u'认证' in value


def transfer_owner(value):
    return isinstance(value, basestring) and (u'否' in value and 1 or 0) or value.rstrip(u'次')


def has_maintenance_record(value):
    u'''
>>> has_maintenance_record('1')
u'\\u662f'
    '''
    return value == '1' and u'是' or u'否'


def phone(value):
    '''
>>> phone('18501050030')
'18501050030'
>>> phone('4000802020')
'4000802020'
    '''
    return len(value) >= 10 and value or None


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
