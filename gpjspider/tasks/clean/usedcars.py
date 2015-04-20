# -*- coding: utf-8 -*-
"""
关于优质二手车清洗的任务
"""
from decimal import Decimal
from datetime import datetime, timedelta
from prettyprint import pp_str
from sqlalchemy.exc import IntegrityError
from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from gpjspider.items import UsedCarItem
from gpjspider.models.product import CarSource, CarDetailInfo, CarImage
from gpjspider.services.cars import get_gpj_category
from gpjspider.services.cars import get_gpj_detail_model
# from gpjspider.services.city import get_gongpingjia_city


from gpjspider.tasks.utils import upload_to_qiniu
from gpjspider.utils.constants import QINIU_IMG_BUCKET
from gpjspider.utils import get_mysql_connect


Session = get_mysql_connect()


@app.task(name="clean_usedcar", bind=True, base=GPJSpiderTask)
def clean_usedcar(self, items, *args, **kwargs):
    logger = get_task_logger('clean_usedcar')
    if not isinstance(items, list):
        items = [items]
    logger.debug(u'清理数据,长度:{0}: {1}'.format(len(items), items))
    session = Session()
    for item in items:
        # 本任务只处理UsedCar
        if not isinstance(item, UsedCarItem):
            logger.error(u'item 不是 UsedCar:{0}'.format(pp_str(item)))
            continue
        # 预处理
        item = preprocess_item(item, session, logger)
        # 业务判断
        if not is_normalized(item, logger):
            logger.warning(u'source.id:{0}不符合规则要求'.format(item['id']))
            continue
        # 业务判断通过，后续处理
        # 上传图片，设置thumbnail
        qiniu_url = upload_img(item, logger)
        if not qiniu_url:
            logger.error(u'上传失败：{0}'.format(item['url']))
            qiniu_url = item['imgurls'].split(' ')[0]
        item['thumbnail'] = qiniu_url
        # 确保 time 正确
        if not item.get('time'):
            item['time'] = item['created_on']
        # control 要么是手动，要么是自动
        if u'手动' in item['control']:
            item['control'] = u'手动'
        else:
            item['control'] = u'自动'
        # phone
        # 1.手机号长度不对
        # 2.400号码长度不对
        # 3.座机号码长度不对
        if 'youche.com' == item['domain']:
            item['quality_service'] = u'14天包退 360天保修'
        elif 'haoche51.com' == item['domain']:
            item['quality_service'] = u'1年/2万公里放心质保 14天可退车'

        # 保存到产品表
        car_source = insert_to_carsource(item, session, logger)
        if not car_source:
            msg = u'插入CarSource时失败:source.id:{0}'.format(item['id'])
            logger.error(msg)
            continue
        insert_to_cardetailInfo(item, car_source, session, logger)
        insert_to_carimage(item, car_source, session, logger)
        logger.error(u'清理source.id={0}成功'.format(item['id']))


def preprocess_item(item, session, logger):
    """
    将需要改变值的字段做处理，如 brand_slug等
    city 换成
    """
    # todo: 将 city 进行匹配
    item['city'] = item['city'].strip(u' 市')
    if item['source_type'] == 2:
        item['source_type'] = 'dealer'
    elif item['source_type'] == 3:
        item['source_type'] = 'cpo'
    elif item['source_type'] == 4:
        item['source_type'] = 'personal'
    elif item['source_type'] == 5:
        item['source_type'] = 'odealer'

    # 默认item['price_bn']是省下的价格
    if 'che.ganji.com' in item['domain'] and item['price'] and item['price_bn']:
        item['price_bn'] += item['price']

    gpj_category = get_gpj_category(
        item['brand_slug'], item['model_slug'], item['domain'])
    if not gpj_category:
        logger.warning(u'无法匹配brand:{0},{1},{2}'.format(
            item['brand_slug'], item['model_slug'], item['domain']))
        item['brand_slug'] = item['model_slug'] = None
    else:
        item['brand_slug'] = gpj_category.parent
        item['model_slug'] = gpj_category.slug
        gpj_detail_model = get_gpj_detail_model(
            gpj_category, item['dmodel'], item['domain'])
        if gpj_detail_model:
            item['detail_model'] = gpj_detail_model.detail_model_slug
        else:
            logger.warning(u'无法匹配到detail_model：{0},{1},{2}'.format(
                gpj_category.id, item['dmodel'], item['domain']))
    return item


def is_normalized(item, logger):
    """
    判断是否符合业务需要

    先不判断 time(item),
    """
    ret = [
        title(item, logger), year(item, logger), month(item, logger),
        mile(item, logger), volume(item, logger), control(item, logger),
        price(item, logger), model_slug(item, logger), brand_slug(item, logger),
        city(item, logger), imgurls(item, logger),
        is_certifield_car(item, logger)
    ]
    return all(ret)


#==============================================================================
# 业务要求
# 不作要求的字段： meta、month、url、color\city_slug\region\region_slug\thumbnail
#               contact\phone\company_name\company_url\price_bn\description\
#               domain\mandatory_insurance\business_insurance\examine_insurance
#==============================================================================
def title(item, logger):
    """
    title 只要为真即可
    """
    return item.get('title')


def year(item, logger):
    """
    2007年以后的车
    """
    try:
        year = int(item.get('year', 0))
    except:
        m = u'判断year错误:{0}:{1}:{2}'.format(
            item['id'], item['url'], item['year'])
        logger.error(m)
        return False
    return year > 2007


def month(item, logger):
    """
    """
    a_month = item.get('month')
    try:
        a_month = int(a_month)
    except:
        return False
    else:
        return 0 < a_month <= 12


def time(item, logger):
    """
    1. 没有 time 无法判断，通过
    2. 有time 的，在一个月之内
    """
    t = item.get('time')
    if not t:
        return True
    if isinstance(t, basestring):
        t = datetime.strptime(t.strip(), '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    a = now - timedelta(days=30) < t < now
    logger.info('time:{0}, result: {1}'.format(time, str(a)))
    return a


def mile(item, logger):
    """
    1. mile < 5
    """
    m = item['mile']
    if isinstance(m, basestring):
        m = Decimal(m)
    if m > 30:
        m = u'判断mile错误:{0}:{1}:{2}'.format(
            item['id'], item['url'], item['mile'])
        logger.error(m)
        return False
    return True


def volume(item, logger):
    """
    volume 需要有值，没有时尝试从款型中获取，获取不到则不要
    todo  try from detail model
    """
    return item.get('volume')


def control(item, logger):
    """
    """
    return item.get('control')


def price(item, logger):
    """
    价格至少1000吧:)
    """
    price = item.get('price')
    return price > 0.0


def brand_slug(item, logger):
    """
    没有品牌不行
    """
    return item.get('brand_slug')


def model_slug(item, logger):
    """
    没有款型不行
    """
    return item.get('model_slug')


def phone(item, logger):
    """
    """
    pass


def city(item, logger):
    """
    没有城市不行
    """
    return item.get('city')


def imgurls(item, logger):
    """
    没有图片不行，但可以没有缩略图，这时使用第一张图片
    nopic： 图片里不能有默认图片
    """
    imgurls = item.get('imgurls')
    if imgurls:
        return 'nopic' not in imgurls
    else:
        return False


def is_certifield_car(item, logger):
    """
    优质二手车的is_certifield_car必须为 真
    """
    return item.get('is_certifield_car')


#==============================================================================
# 数据库操作
#==============================================================================
def insert_to_carsource(item, session, logger):
    """
    """
    car_source = CarSource()
    car_source.url = item['url']
    car_source.title = item['title']
    car_source.pub_time = item['time'] if item['time'] else item['created_on']
    car_source.brand_slug = item['brand_slug']
    car_source.model_slug = item['model_slug']
    car_source.model_detail_slug = item['detail_model']
    car_source.mile = item['mile']
    car_source.year = item['year']
    car_source.month = item['month']
    car_source.control = item['control']
    car_source.city = item['city']
    car_source.price = item['price']
    car_source.volume = item['volume']
    car_source.color = item['color']
    car_source.thumbnail = item['thumbnail']
    car_source.phone = item['phone']
    car_source.domain = item['domain']
    car_source.source_type = item['source_type']
    car_source.status = 'sale'

    session.add(car_source)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.error(u'成功保存:重复:{0}'.format(car_source.url))
    except Exception as e:
        logger.error(u'未知异常:{0}\n{1}'.format(car_source.url, unicode(e)))
    else:
        logger.info(u'成功保存:{0}'.format(car_source.url))
    return car_source


def insert_to_cardetailInfo(item, car_source, session, logger):
    car_detail_info = CarDetailInfo()
    car_detail_info.car = car_source
    car_detail_info.condition = item.get('condition_detail')
    car_detail_info.examine_insurance = item.get('examine_insurance')
    car_detail_info.business_insurance = item.get('business_insurance')
    car_detail_info.mandatory_insurance = item.get('mandatory_insurance')
    car_detail_info.company_name = item.get('company_name')
    car_detail_info.region = item.get('region')
    car_detail_info.contact = item.get('contact')
    car_detail_info.description = item.get('description')
    car_detail_info.transfer_owner = item.get('transfer_owner')
    car_detail_info.maintenance = item.get('maintenance_desc')
    car_detail_info.insurance_money = None
    car_detail_info.car_key = None
    car_detail_info.quality_assurance = item.get('quality_service')
    car_detail_info.condition_score = item.get('condition_level')
    session.add(car_detail_info)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        msg = u'成功保存:重复:car_detail_info:car_source:{0}'.format(car_source.id)
        logger.error(msg)
    except Exception as e:
        logger.error(u'未知异常:{0}\n{1}'.format(car_source.url, unicode(e)))
    else:
        logger.info(u'成功保存:car_detail_info:{0}'.format(car_detail_info.id))
    return car_detail_info


def insert_to_carimage(item, car_source, session, logger):
    """
    """
    imgs = item['imgurls'].split(' ')
    for img in imgs:
        car_image = CarImage()
        car_image.car = car_source
        car_image.image = img
        session.add(car_image)
        logger.debug(u'添加CarImage：{0}'.format(img))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        msg = u'成功保存:重复:CarImage:car_source:{0}'.format(car_source.id)
        logger.error(msg)
    except Exception as e:
        logger.error(u'未知异常:{0}\n{1}'.format(car_source.url, unicode(e)))
    else:
        logger.info(u'成功保存:CarImage:{0}'.format(car_source.id))


#==============================================================================
# utils 函数
#==============================================================================

def upload_img(item, logger):
    """
    """
    thumbnail = item.get('thumbnail')
    if not thumbnail:
        thumbnail = item['imgurls'].split(' ')[0]
    if thumbnail:
        logger.info(u'上传 thumbnail：{0}'.format(thumbnail))
        qiniu_url = upload_to_qiniu(thumbnail, QINIU_IMG_BUCKET)
        if qiniu_url:
            logger.info(u'上传 thumbnail成功：{0}'.format(qiniu_url))
            return 'http://gongpingjia.qiniudn.com/' + qiniu_url
        else:
            logger.info(u'上传 thumbnail失败：{0}'.format(thumbnail))
            return None
    else:
        logger.error(u'没有 thumbnail，原始 URL：{0}'.format(item['url']))
        return None
