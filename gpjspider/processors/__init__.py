# -*- coding: utf-8 -*-
from decimal import Decimal
import re
import pdb
# pdb.set_trace()
from datetime import datetime, timedelta
from dateutil.parser import parse
from exceptions import TypeError
try:
    from gpjspider.utils.phone_parser import ConvertPhonePic2Num
except Exception, e:
    print e

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


def first(values):
    if isinstance(values, (list, tuple)):
        for value in values:
            value = strip(value)
            if value:
                return value
        # return strip(values[0])
    else:
        return values


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


def control(value):
    if not value:
        return
    match = re.findall(u'([手自]{1,2}一?[动体])', value)
    if match:
        value = match[0]
    return value


def quality_service(values):
    u'''
>>> quality_service(u'质保到期： 已过期,延长质保： ,24,个月/,9.9,万公里&nbsp;(自您购车日起算)'.split(','))
u'\\u8d28\\u4fdd\\u5230\\u671f\\uff1a\\u5df2\\u8fc7\\u671f, \\u5ef6\\u957f\\u8d28\\u4fdd\\uff1a24\\u4e2a\\u6708/9.9\\u4e07\\u516c\\u91cc&nbsp;(\\u81ea\\u60a8\\u8d2d\\u8f66\\u65e5\\u8d77\\u7b97)'
>>> quality_service(u'质保到期： test,原厂延保： ,24,个月/,9.9,万公里&nbsp;(自您购车日起算)'.split(','))
u'\\u8d28\\u4fdd\\u5230\\u671f\\uff1atest, \\u539f\\u5382\\u5ef6\\u4fdd\\uff1a24\\u4e2a\\u6708/9.9\\u4e07\\u516c\\u91cc&nbsp;(\\u81ea\\u60a8\\u8d2d\\u8f66\\u65e5\\u8d77\\u7b97)'
    '''
    value = isinstance(values, (list, tuple)) and concat(
        values).replace(' ', '') or values
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
    return a and gpjfloat(a[0]) or 0


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
>>> model_slug(u'1-test2013款')
u'test'
>>> model_slug(u'1-test13款')
u'test'
>>> model_slug(u'1  test')
u'test'
>>> model_slug(u'test >')
u'test'
>>> model_slug(u'a-test')
u'test'
>>> model_slug(u'二手test')
u'test'
    '''
    # pdb.set_trace()
    value = value.strip('> ').lstrip(u'二手')
    if ' ' in value:
        a = reg_blank_split.split(value)
        return a[1]
    elif '-' in value:
        a = value.split('-')
        value = a[1]
        match = re.findall(u'([^21]+)\d{2,4}款', value)
        return match and match[0] or value
    else:
        return value


def city(value):
    u'''
>>> city(u'河北 石家庄')
u'\\u77f3\\u5bb6\\u5e84'
>>> city(u'test二手车市>')
u'test'
>>> city(u'二手A城')
u'A\\u57ce'
    '''
    if ' ' in value:
        value = value.split()[-1]
    else:
        value = re.sub(u'[二手车]{2,}.*$', '', value.lstrip(u'二手'))
        # value = re.sub(ur'车.*$', '', value.strip(u'二手'))
        # value = value.strip(u'二手车商市> ')
    return value.rstrip(u'市')


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


# def status(value):
    # if value == '1':
    # return True
    # elif value == '0':
    # return False
    # return bool(value)

# def source_type(value):

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
>>> price(u'面议万元')
Decimal('0.0')
    '''
    v = extract(value, ur'[^\d]*(\d*\.?\d{1,2})万', decimal)
    if isinstance(v, basestring) and value and not u'万' in value:
        v = extract(value, ur'[^\d]*(\d*\.?\d{1,2})', decimal)
    if isinstance(v, Decimal) and v > 10000:
        v /= 10000
    if isinstance(v, Decimal):
        return v
    else:
        return Decimal('0.0')
    # return v


def price_bn(value):
    u'''
>>> price_bn(u'新车指导价：39.8万')
Decimal('39.8')
>>> price_bn(u'新车价：29.88万+2.56万（购置税）')
Decimal('29.88')
>>> price_bn(u'新车：31.80万 + 2.72万购置税')
Decimal('31.80')
>>> price_bn(u'新车价： \\n8.98万+0.77万购置税，比新车省')
Decimal('8.98')
>>> price_bn(u'(裸车价44.95万元+购置税3.84万元)')
Decimal('44.95')
    '''
    # print value
    v = extract(value, ur'[新车指导价]{2,5}\D*[^\d]{,2}(\d*\.?\d{1,2})万?', decimal)
    if isinstance(v, basestring) and value and not u'万' in value:
        v = extract(value, ur'[新车指导价]{2,5}\D*[^\d]{,2}(\d*\.?\d{1,2})', decimal)
    if isinstance(v, Decimal) and v > 10000:
        v /= 10000
    return v if isinstance(v, Decimal) else None


def mile(value):
    u'''
>>> mile(u'0.1万公里')
Decimal('0.1')
>>> mile(u'26.78        万公里')
Decimal('26.78')
>>> mile(u'7万公里')
Decimal('7')
>>> mile(u'3000万公里')
Decimal('0.3')
>>> mile(u'55')
Decimal('0.0055')
>>> mile(u'600公里')
Decimal('0.06')
>>> mile(u'600')
Decimal('0.06')
>>> mile(u'三十二万公里')
unsupported operand type(s) for /=: 'unicode' and 'int' 三十二万公里
>>> mile(u'138,100公里')
Decimal('13.81')
    '''

    # print v
    # if isinstance(v, Decimal) and v > 150 or value and not u'万' in value:
    if isinstance(value, basestring):
        value = re.sub(',', '', value)
        if not u'万' in value:
            v = extract(value, ur'(\d+|[\d\.]{3,})公里', decimal)
            v /= 10000
        else:
            v = extract(value, ur'[^\d]*(\d+|[\d\.]{3,})\s*万公里', decimal)
    else:
        v = value
    try:
        v = decimal(v)
        # v = extract(value, ur'(\d+)公里', decimal)
        if v > 1000:
            v /= 10000
    except Exception as e:
        print e, v
        return None
    return v


def gpj_now():
    return datetime.now()


def year(value, max_year=gpj_now().year):
    u'''
>>> year('2007-1')
2007
>>> year(u'2014年09月')
2014
>>> year(u'2014年')
2014
>>> year(u'09年')
2009
    '''
    y = extract(extract(value, u'(\d{4}).\d{1,2}', gpjint), ur'(\d{2,4}).', gpjint)
    if isinstance(y, int) and y < 99:
        try:
            y = int(y) + 2000
            if y > max_year:
                y -= 100
        except:
            pass
    return y


def month(value):
    u'''
>>> month('2007-1')
1
>>> month(u'2014年09月')
9
>>> month(u'2012年3月')
3
>>> month(u'2012年')
    '''
    m = extract(value, ur'\d{4}.(\d{1,2})', gpjint)
    return m if isinstance(m, int) and m < 13 else None


def get_overdue_date():
    date = gpjtime_bytimedelta(u'1周前')
    return u'-'.join([str(e) for e in [date.year, date.month, 1]])


def year_month(value):
    u'''
>>> year_month(u'保险到期： 2014-7')
u'2014-7-1'
>>> year_month(u'2014-8-12')
u'2014-8-1'
>>> year_month(u'2014')
'2014-1-1'
>>> year_month(u'已过期').endswith('-1')
True
>>> year_month(u'已到期').endswith('-1')
True
    '''
    regx = re.compile(ur'(\d{4}).(\d{1,2})')
    a = regx.findall(value)
    if a:
        a = a[0]
        # print a
        return u'-'.join(a) + (len(a) == 3 and '' or '-1')
    else:
        if u'已过期' in value or u'已到期' in value:
            value = get_overdue_date()
        else:
            value = year(value)
            value = '%s-1-1' % value if isinstance(value, int) else None
        return value

mandatory_insurance = year_month
business_insurance = year_month
examine_insurance = year_month


def str_to_unicode(value, encoding):
    return unicode(value, encoding) if isinstance(value, str) else value


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
    elif u'今天' in time:
        time = u'0天前'
    elif u'昨天' in time:
        time = u'1天前'
    elif u'前天' in time:
        time = u'2天前'
    elif u'半小时前' in time:
        time = u'30分钟前'
    t = gpjtime_bytimedelta(time)
    time = t if isinstance(t, datetime) else gpjtime_byfmt(t)
    return to_str and time and str(time)[:19] or time

time = gpjtime


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
True
>>> isinstance(gpjtime_bytimedelta(u'1年前'), datetime)
False
    """
    time = str_to_unicode(time, encoding)
    tag = [(u'秒前', 'S', 1), (u'分钟前', 'S', 60), (u'小时前', 'S', 3600),
           (u'天前', 'D', 1),  (u'周前', 'D', 7), (u'星期前', 'D', 7),
           # (u'个月前', 'D', 30), (u'月前', 'D', 30),
           (u'个月前', 'M', 1), (u'月前', 'M', 1),
           ]
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


def clean_anchor(url):
    '''
>>> clean_anchor('http://www.che168.com/dealer/85459/4807604.html#pvareaid=100519')
'http://www.che168.com/dealer/85459/4807604.html'
>>> clean_anchor('/autonomous/4650620.html#pvareaid=100522#pos=11')
'/autonomous/4650620.html'
    '''
    return extract(url, '([^#]+)#?.*')


def clean_param(url):
    '''
>>> clean_param('http://www.taoche.com/buycar/b-DealerSHTY1149889S.html?mz_ca=2004885&mz_sp=6sk40')
'http://www.taoche.com/buycar/b-DealerSHTY1149889S.html'
    '''
    return url.split('?')[0]


def clean_space(value):
    return value.replace(' ', '')


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


def remove_param(url, param):
    '''
>>> remove_param('http://jinhua.baixing.com/ershouqiche/a796036346.html?index=82', 'index')
'http://jinhua.baixing.com/ershouqiche/a796036346.html'
    '''
    return re.sub('[\?&]%s=[^&]*' % param, '', url)


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
>>> dmodel(u'贵阳白云区  比亚迪S7 2015款 2.0T 手自一体 旗舰型 (国Ⅴ)')
u'2015\\u6b3e 2.0T \\u624b\\u81ea\\u4e00\\u4f53 \\u65d7\\u8230\\u578b (\\u56fd\\u2164)'
    '''
    if value:
        value = extract(value, u'(\d{2}款.+|\d{4}款.+)$').replace('  ', ' ')
    return value


def raw_imgurls(value):
    return


def is_certifield_car(value):
    u'''
>>> is_certifield_car(u'原厂质保')
True
>>> is_certifield_car(True)
True
    '''
    return any([value == '1', u'质保' in value, u'保障' in value, u'认证' in value,
                u'7天可退' in value, u'原厂联保' in value, u'包退' in value, u'保修' in value]) \
        if isinstance(value, basestring) else bool(value)
is_certified = is_certifield_car


def transfer_owner(value):
    u'''
>>> transfer_owner(u'一手车')
0
    '''
    if isinstance(value, basestring):
        if any([u'否' in value, u'二手' in value]):
            return 1
        elif any([u'是' in value, u'一手' in value]):
            return 0
        elif re.match('^[1-9]+', value):
            return int(re.match('^[1-9]+', value).group())
        else:
            return 0
    return value
    # return (1 if any([u'否' in value, u'二手' in value]) else 0 if any([u'是' in value, u'一手' in value]) \
    # else int(value.rstrip(u'次')) \
    #)  if isinstance(value, basestring) else value


def description(value):
    return value.strip()


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
>>> phone('181-1715-1473')
'18117151473'
>>> phone('4000802020-530867')
'4000802020-530867'

# >>> phone('http://cache.taoche.com/buycar/gettel.ashx?u=6020852&t=taabcimate')
# 'http://cache.taoche.com/buycar/gettel.ashx?u=6020852&t=taabcimate#4008159042#0.99'
    '''
    if value and len(value) >= 10:
        if value.startswith('http://'):
            return value
            try:
                phone_info = ConvertPhonePic2Num(value).find_possible_num()
                value += '#%s#%s' % phone_info
                return value
            except Exception as e:
                print e
        if len(value.split('-')) > 2:
            value = value.replace('-', '')
        value = re.sub('\(.+\)', ' ', value).strip()
    else:
        value = None
    return value


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
