# -*- coding: utf-8 -*-
import re
from gpjspider.models.product import CategoryDict
from gpjspider.models.product import NormalModelDetail
from gpjspider.models.product import ByYearVolume
from gpjspider.utils import get_mysql_connect
try:
    import ipdb
except ImportError:
    import pdb as ipdb

__ALL__ = (
    'get_gpj_category', 'get_gpj_detail_model', 'process_detail_model_string'
)
Session = get_mysql_connect()


def get_average_price(brand, model, year, volume):
    u"""
    获取平均价格
    """
    session = Session()
    q = session.query(ByYearVolume).filter_by(brand_slug=brand, model_slug=model,
                                              year=year, volume=volume)
    return q.first()

xin_model_url = lambda x: re.sub(r'/\w+/s', '/quanguo/s', x)

def get_gpj_category(brand, model, domain, session=None, model_url=None):
    u"""
>>> cat = get_gpj_category(u'凯迪拉克', u'凯雷德ESCALADE', 'souche.com')
>>> cat.slug
u'escalade'
    """
    session = session or Session()
    query = session.query(CategoryDict)
    query = query.filter_by(domain=domain, name=model, parent=brand).filter(
        CategoryDict.global_slug!=None,
        CategoryDict.global_name!=None
    )
    #ipdb.set_trace()
    amount = query.count()
    if amount>0:
        query = query.first()
        return query.category or None
    elif model_url:
        info = dict(url=model_url)
        if domain in ['xin.com']:
            match = re.findall('/s(\d+)/', model_url)
            if match:
                info = dict(slug=match[0])
            # model_url = xin_model_url(model_url)
        elif domain in ['taoche.com']:
            match = re.findall('com/([\d\w]+)/$', model_url)
            if match:
                info = dict(slug=match[0])
            # model_url = xin_model_url(model_url)
        query = query.filter_by(domain=domain, **info)
        amount = query.count()
        if amount>0:
            query = query.first()
            return query and query.category or None
        # print amount, domain, brand, model, model_url
    return amount


def get_gpj_detail_model(gpj_slug, detail_model_str, domain):
    u"""
    gongpingjia_slug是Category.slug
    detail_model_string是抓取的款型
    todo
    """
    session = Session()
    detail_model_string = process_detail_model_string(detail_model_str, domain)
    q = session.query(NormalModelDetail).filter(
        NormalModelDetail.global_slug == gpj_slug.slug)
    q = q.filter(NormalModelDetail.model_detail == detail_model_string).first()
    if not q:
        return None
    return q.obj_model_detail


def process_detail_model_string(detail_model_string, domain):
    u"""
    因为不同网站上显示的detail_model_string和它们的数据库形式有些区别，根据发现的区别
    进行调整，以便在数据库中能匹配上。
    """
    domains = {
        'haoche51.com': __process_haoche51,
        'c.cheyipai.com': __process_cheyipai,
    }
    process_func = domains.get(domain)
    #  没有函数处理 detail_model_string，返回原样，看能否匹配到
    if not process_func:
        return detail_model_string
    else:
        return process_func(detail_model_string)


def __process_haoche51(detail_model_string):
    u"""
    奥迪 A6L 2011款 2.4L 舒适型
    好车无忧的标题由4部分组成：
    品牌 型号 年份 款型
    """
    return detail_model_string.split(' ', 3)[-1]

def __process_cheyipai(detail_model_string):
    u"""
    cheyipai 的前两部分是品牌和型号，剩下是款型
    """
    ss = re.split(ur'\s+', detail_model_string)
    return u' '.join(ss[2:])

def get_price():
    pass


def test():
    print '%r' % get_gpj_category(u'凯迪拉克', u'凯雷德ESCALADE', 'souche.com')

if __name__ == '__main__':
    # test()
    import doctest
    print(doctest.testmod())
