# -*- coding: utf-8 -*-
import re
from gpjspider.models.product import CategoryDict
from gpjspider.models.product import NormalModelDetail
from gpjspider.models.product import ByYearVolume
from gpjspider.utils import get_mysql_connect

__ALL__ = (
    'get_gpj_category', 'get_gpj_detail_model', 'process_detail_model_string'
)
Session = get_mysql_connect()


def get_average_price(brand, model, year, volume):
    """
    获取平均价格
    """
    session = Session()
    q = session.query(ByYearVolume).filter(ByYearVolume.brand_slug == brand)
    q = q.filter(ByYearVolume.model_slug == model)
    q = q.filter(ByYearVolume.year == year)
    q = q.filter(ByYearVolume.volume == volume)
    return q.first()


def get_gpj_category(brand, model, domain):
    """
    """
    session = Session()
    q = session.query(CategoryDict).filter(CategoryDict.name == model)
    q = q.filter(CategoryDict.parent == brand)
    q = q.filter(CategoryDict.domain == domain)
    d = q.first()
    if not d:
        return None
    else:
        return d.category


def get_gpj_detail_model(gpj_slug, detail_model_str, domain):
    """
    gongpingjia_slug是Category.slug
    detail_model_string是抓取的款型
    todo
    """
    session = Session()
    # 转换一下以便能在数据库中匹配到
    detail_model_string = process_detail_model_string(detail_model_str, domain)
    q = session.query(NormalModelDetail).filter(
        NormalModelDetail.global_slug == gpj_slug.slug)
    q = q.filter(NormalModelDetail.model_detail == detail_model_string).first()
    if not q:
        return None
    return q.obj_model_detail


def process_detail_model_string(detail_model_string, domain):
    """
    因为不同网站上显示的detail_model_string和它们的数据库形式有些区别，根据发现的区别
    进行调整，以便在数据库中能匹配上。
    """
    domains = {
        'renrenche.com': __process_renrenche,
        'haoche51.com': __process_haoche51,
        'haoche.ganji.com': __process_ganjihaoche,
        'c.cheyipai.com': __process_cheyipai,
        'xin.com': __process_xin,
        'souche.com': __process_souche,
        'youche.com': __process_youche,
        '99haoche.iautos.cn': __process_99haoche,
    }
    process_func = domains.get(domain)
    #  没有函数处理 detail_model_string，返回原样，看能否匹配到
    if not process_func:
        return detail_model_string
    else:
        return process_func(detail_model_string)


def __process_renrenche(detail_model_string):
    return detail_model_string


def __process_haoche51(detail_model_string):
    """
    奥迪 A6L 2011款 2.4L 舒适型
    好车无忧的标题由4部分组成：
    品牌 型号 年份 款型
    """
    return detail_model_string.split('', 3)[-1]


def __process_ganjihaoche(detail_model_string):
    return detail_model_string


def __process_cheyipai(detail_model_string):
    """
    cheyipai 的前两部分是品牌和型号，剩下是款型
    """
    ss = re.split(ur'\s+', detail_model_string)
    return u' '.join(ss[2:])


def __process_xin(detail_model_string):
    return detail_model_string


def __process_souche(detail_model_string):
    """
    大搜车  标题就是款型
    """
    return detail_model_string


def __process_youche(detail_model_string):
    return detail_model_string


def __process_99haoche(detail_model_string):
    return detail_model_string


def get_price():
    """
    """
    pass
