# -*- coding: utf-8 -*-
"""
关于优质二手车清洗的任务
"""
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from gpjspider.items import UsedCarItem
from gpjspider.models.product import CarSource, CarDetailInfo, CarImage
from gpjspider.models import UsedCar, TradeCar
from gpjspider.services.cars import get_gpj_category
from gpjspider.services.cars import get_gpj_detail_model
from gpjspider.services.cars import get_average_price
# from gpjspider.services.city import get_gongpingjia_city


from gpjspider.tasks.utils import upload_to_qiniu, batch_upload_to_qiniu
from gpjspider.utils.constants import QINIU_IMG_BUCKET
from gpjspider.utils.phone_parser import ConvertPhonePic2Num
from gpjspider.utils import get_mysql_connect, get_mysql_cursor as get_cursor
from gpjspider.processors import souche
from celery import group
import threading
import pdb
from time import sleep


class async(object):
    ''' Decorator that turns a callable function into a thread.'''

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        thread = threading.Thread(
            target=self.func,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        return True

Session = get_mysql_connect()


@app.task(name="clean_domain", bind=True, base=GPJSpiderTask)
def clean_domains(self, sync=False, amount=500):
    domains = '99haoche.com souche.com youche.com'.split()
    group(clean_domain.s(domain, sync, amount) for domain in domains)


def log(msg, *args):
    print str(datetime.now())[11:19], msg,
    for arg in args:
        print arg,
    print ''

@app.task(name="clean_domain", bind=True, base=GPJSpiderTask)
def clean_domain(self, domain=None, sync=True, amount=50, per_item=10):
# def clean_domain(self, domain=None, sync=False, amount=50, per_item=10):
    log('Starting..')
    session = Session()
    cursor = get_cursor()
    domains = domain and [domain] or \
        [
        'xin.com', 'ygche.com.cn',
        'haoche51.com', 'renrenche.com',
        '99haoche.com', 'haoche.ganji.com', 'souche.com', 'youche.com',
        #'c.cheyipai.com',
        '58.com', '2sc.sohu.com', 'taoche.com',
        'ganji.com', '51auto.com', 'baixing.com',
        ]
    # created_on>=curdate()  between '2015-05-1' and '2015-05-10' '2015-05-10' and '2015-05-20'  and id>17549018
    # update = "update open_product_source set status='C' where source_id=1 \ , 'E'
    # update = "update open_product_source set status='C' where created_on > '2015-06-18' and source_id=1 \
    # update = "update open_product_source set status='C' where created_on>=curdate() and source_id=1 \ a.domain='ygche.com.cn'
        # where created_on between '2015-6-26' and '2015-7-2' and source_id=1 \
    update = "update open_product_source a, car_source b set a.status='C' \
        where created_on>=curdate() and source_id=1 \
        and a.url=b.url and a.status in ('I');"
    if sync:
        cursor.execute(update.format("','".join(domains)))
    sql = session.query(UsedCar.id).filter_by(status='Y', source=1
        ).filter(UsedCar.domain.in_(domains),
        UsedCar.created_on >= str(datetime.now())[:10],
        # UsedCar.created_on >= '2015-07-1',
        # UsedCar.created_on < str(datetime.now())[:10],
        # UsedCar.status.in_(['N', 'Y']),
        )
    min_id = sql.first().id
    # max_id = sql.order_by('-id').first().id
    select = 'select %s(id) from open_product_source where status="Y" and source_id=1 and domain in (\'%s\');'
    max_id = cursor.execute(select % ('max', "','".join(domains))).fetchone()[0]
    clean_source(session, min_id, max_id, domains, cursor)

    if max_id > min_id:
        print min_id, max_id - min_id
        cursor.execute('update open_product_source set status="N" \
            where source_id=1 and id between %s and %s and status="Y" \
            and domain in (\'%s\');' % (min_id, max_id, "','".join(domains)))
        push_trade_cars(session, min_id, max_id, domains)
    log('Done')

WORKER = 20
# WORKER = 10
WORKER = 40

def clean_source(session, min_id, max_id, domains, cursor):
    query = session.query(UsedCar.id).filter_by(source=1, is_certifield_car=True,
        status='Y',
        # id=20677378 # 243410 19688565
        ).filter(
            # UsedCar.created_on >= str(datetime.now())[:10],
            UsedCar.id >= min_id,
            UsedCar.id <= max_id,
            # UsedCar.status.in_(['i', 'I', 'Y']),
            #UsedCar.status.in_(['E', 'model_slug']),
            #UsedCar.model_url is not None,
            # UsedCar.status.in_(['E', 'I', 'Y']),
            #UsedCar.created_on > '2015-06-18',
            # UsedCar.created_on <= '2015-05-18',
            # UsedCar.created_on >= '2015-05-1',
            # UsedCar.created_on >= '2015-05-15',
            # UsedCar.status.in_(['N', 'Y']),
            # UsedCar.status.in_(['i', 'I']),
            # UsedCar.status.in_(['i', 'I', 'model_slug']),
            UsedCar.domain.in_(domains),
            UsedCar.phone != None, UsedCar.model_slug != None, UsedCar.imgurls != None, UsedCar.control != None,
            UsedCar.price > 0, UsedCar.volume > 0, UsedCar.year > 2007, UsedCar.mile < 30
            )
    remain = query.count()
    # print remain
    index = 0
    psize = 10
    # psize = 30
    # psize = 60
    # psize = 100
    amount = (remain / psize)
    items = []
    global WORKER
    waits = 4
    first = True
    for item in query.yield_per(psize):
        index += 1
        items.append(str(item.id))
        if index % psize == 0:
            ids = items
            if first:
                log(amount, '%s - %s' % (min(ids), max(ids)))
                first = False
            cursor.execute('update open_product_source set status="I" where id in (%s)' % ','.join(ids))
            async_clean(clean_usedcar, items)
            amount -= 1
            # sleep(3 if WORKER < 5 else 2)
            sleep(2 if WORKER < 5 else 1)
            while WORKER == 0:
                sleep(waits)
            items = []

    if items:
        ids = items
        log(amount, '%s - %s' % (min(ids), max(ids)))
        async_clean(clean_usedcar, items)
        # sync_clean(clean_usedcar, items)
        # session.commit()

def push_trade_cars(session=Session(), min_id=None, max_id=None, domains=None):
    filt = []
    if min_id:
        filt.append(UsedCar.id >= min_id)
        if not max_id:
            max_id = min_id
    if max_id:
        filt.append(UsedCar.id <= max_id)
    # elif not min_id:
    #     filt.append(UsedCar.created_on >= str(datetime.now())[:10])
    if domains:
        filt.append(UsedCar.domain.in_(domains))
    # print filt, locals()
    query = session.query(UsedCar.id).filter_by(source=1, source_type=4,
        status='N', checker_runtime=1
        # id=20778181 # 243410 19688565
        ).filter(
            # UsedCar.created_on >= str(datetime.now())[:10],
            UsedCar.brand_slug != None,
            UsedCar.phone.startswith('1'),
            UsedCar.model_slug != None,
            UsedCar.volume is not None,
            UsedCar.year > 0,
            UsedCar.mile < 200,
            *filt
            )
    remain = query.count()
    index = 0
    psize = 10
    # psize = 100
    amount = (remain / psize)
    items = []
    waits = 3
    meth = push_trade_car
    global WORKER
    for item in query.yield_per(psize):
        index += 1
        items.append(str(item.id))
        if index % psize == 0:
            async_clean(meth, items)
            amount -= 1
            while WORKER == 0:
                sleep(waits)
            items = []

    if items:
        sync_clean(meth, items)

def push_trade_car(items):
    session = Session()
    for item in items:
        sid = str(item['id'])
        # print sid
        if not is_trade_car(item):
            continue
        match_bmd(item)
        if not item['brand_slug']:
            continue
        try:
            car = TradeCar.init(item)
            session.add(car)
            session.commit()
            session.query(UsedCar).filter_by(id=sid).update(
                dict(checker_runtime_id=0), synchronize_session=False)
        except IntegrityError:
            session.rollback()
        except Exception as e:
            print e, sid
    session.close()

@async
def async_clean(func, items, *args, **kwargs):
    sync_clean(func, items, *args, **kwargs)

def sync_clean(func, items, *args, **kwargs):
    global WORKER
    WORKER -= 1
    if isinstance(items[0], basestring):
        ids = items
        items = []
        session = Session()
        for item in session.query(UsedCar).filter(UsedCar.id.in_(ids)).yield_per(10):
            items.append(item.__dict__)
        session.close()
    func(items, *args, **kwargs)
    # get_cursor().execute('update open_product_source set checker_runtime_id=0 \
    #     where id in (%s);' % ','.join(ids))
    WORKER += 1


def update_item(item, **kwargs):
    for k, v in kwargs.items():
        if not item.get(k):
            item[k] = v

def is_trade_car(item):
    if all([
        item['source_type'] == 4,
        item['city'] in [u'\u5317\u4eac', u'\u6210\u90fd', u'\u5357\u4eac'],
        item['volume'],
        item['phone'].startswith('1') and len(item['phone']) == 11,
        ]):
        return True
    return False

@app.task(name="clean_usedcar", bind=True, base=GPJSpiderTask)
def clean_usedcar(self, items, *args, **kwargs):
    logger = get_task_logger('clean_usedcar')
    if not isinstance(items, list):
        items = [items]
    logger.debug(u'清理数据,长度:{0}: {1}'.format(len(items), items))
    status = {
        'C': [],
        'P': [],
        'E': [],
        'S': [],
    }
    session = Session()
    for item in items:
        if isinstance(item, UsedCarItem):
            item = item._values
            continue

        sid = str(item['id'])
        # print sid

        try:
            item = preprocess_item(item, session, logger)
            flag = is_normalized(item, logger)
            if flag is not True:
                logger.warning(u'source.id: {0} 不符合规则要求'.format(sid))
                if sid:
                    key = flag if isinstance(flag, basestring) else 'P'
                    if key not in status:
                        status[key] = []
                    status[key].append(sid)
                continue
            if is_trade_car(item):
                car = TradeCar.init(item)
                try:
                    session.add(car)
                    session.commit()
                    session.query(UsedCar).filter_by(id=sid).update(
                        dict(checker_runtime_id=0), synchronize_session=False)
                    # logger.debug(u'Saved trade_car {0}'.format(car.id))
                except IntegrityError:
                    session.rollback()
                except Exception as e:
                    print e
            # 确保 time 正确
            if not item.get('time'):
                item['time'] = item['created_on']
            # control 要么是手动，要么是自动
            control = item['control']
            if any([u'手动' in control, 'MT' in control, 'mt' in control]):
                item['control'] = u'手动'
            else:
                item['control'] = u'自动'
            # phone
            # 1.手机号长度不对
            # 2.400号码长度不对
            # 3.座机号码长度不对
            # TODO: add phone validation
            domain = item['domain']
            if 'youche.com' == domain:
                update_item(item, quality_service=u'14天包退 360天保修', contact=u'优车诚品客服',
                    company_name=u'优车诚品', company_url='http://www.youche.com',
                    region=u'北京亦庄经济技术开发区经海三路科创六街95号', phone='4000-990-888')
            elif 'haoche51.com' == domain:
                update_item(item, quality_service=u'1年/2万公里放心质保 14天可退车',
                    company_name=u'好车无忧', company_url='http://www.haoche51.com',
                    contact=u'好车无忧客服', phone='400-801-9151')
            elif 'haoche.ganji.com' == domain:
                update_item(item,
                    company_name=u'赶集好车', company_url='http://haoche.ganji.com',
                    contact=u'赶集好车客服', phone='400-733-6622')
            #elif 'c.cheyipai.com' == domain:
            #    update_item(item,
            #        company_name=u'车易拍客服', company_url='http://c.cheyipai.com',
            #        contact=u'车易拍客服', phone='400-733-6622')

            # 业务判断通过，后续处理
            upload_img(item, logger)
            # upload_imgs(item, logger)

            # 保存到产品表
            car_source = insert_to_carsource(item, session, logger)
            # print car_source.id
            # return
            if not car_source:
                logger.error(u'插入CarSource时失败:source.id:{0}'.format(sid))
                s = 'S'
            else:
                logger.error(u'清理source.id={0}成功'.format(sid))
                s = 'C'
        except Exception as e:
            # raise
            print e, sid
            s = 'E'
        if sid:
            status[s].append(sid)
    cursor = get_cursor(session)
    for k, v in status.items():
        if v:
            # cursor.execute(
            #     'update open_product_source set status="%s" where id in (%s) and status="%s";' % (k.lower(), ','.join(v), k))
            cursor.execute(
                'update open_product_source set status="%s" where id in (%s);' % (k, ','.join(v)))
    session.commit()
    # session.close()

def get_province_by_city(city, session=None):
    res = get_cursor(session).execute(
        'SELECT b.name FROM open_city a, open_city b WHERE a.name="%s" and a.parent=b.id;' % city).fetchone()
    return res[0] if res else None


def preprocess_item(item, session, logger):
    # todo: 将 city 进行匹配
    item['city'] = item['city'].strip(u' 市')
    province = get_province_by_city(item['city'], session)
    if province:
        item['province'] = province
    else:
        item['province'] = None
        # return item

    domain = item['domain']
    if domain in ['58.com']:
        if item['source_type'] in (2, 3):
            item['is_certifield_car'] = True

    if item['source_type'] == 2:
        item['source_type'] = 'dealer'
    elif item['source_type'] == 3:
        item['source_type'] = 'cpo'
    elif item['source_type'] == 4:
        item['source_type'] = 'personal'
    elif item['source_type'] == 5:
        item['source_type'] = 'odealer'

    # 默认item['price_bn']是省下的价格
    if 'che.ganji.com' in domain and item['price'] and item['price_bn']:
        item['price_bn'] += item['price']

    match_bmd(item, domain)
    return item

def match_bmd(item, domain=None):
    domain = domain or item['domain']
    gpj_category = get_gpj_category(
        item['brand_slug'], item['model_slug'], domain, item.get('model_url'))
    if not gpj_category:
        # logger.warning(u'No match model for: {0},{1},{2}'.format(
            # item['brand_slug'], item['model_slug'], domain))
        item['brand_slug'] = item['model_slug'] = None
    else:
        if isinstance(gpj_category, int):
            item['model_slug'] = gpj_category
        else:
            item['brand_slug'] = gpj_category.parent
            item['model_slug'] = gpj_category.slug
            if domain != 'ygche.com.cn':
                gpj_detail_model = get_gpj_detail_model(
                    gpj_category, item['dmodel'], domain)
                if gpj_detail_model:
                    item['detail_model'] = gpj_detail_model.detail_model_slug
                # else:
                #     logger.warning(u'无法匹配到detail_model：{0},{1},{2}'.format(
                #         gpj_category.id, item['dmodel'], domain))


def is_normalized(item, logger):
    funcs = [title, city, price, model_slug, brand_slug, phone, year, month, 
            mile, volume, control, imgurls, maintenance_desc]
    try:
        for func in funcs:
            if not func(item, logger):
                return func.__name__
        return True
    except Exception as e:
        print e, item.get(func.__name__)


#==============================================================================
# 业务要求
# 不作要求的字段： meta、month、url、color\city_slug\region\region_slug\thumbnail
#               contact\phone\company_name\company_url\price_bn\description
#               domain\mandatory_insurance\business_insurance\examine_insurance
#==============================================================================
def title(item, logger):
    return item.get('title')


def year(item, logger):
    """
    year > 2007
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
    a_month = item.get('month')
    try:
        if 0 < int(a_month) <= 12:
            return True
    except:
        pass
    item['month'] = None
    return True


def time(item, logger):
    u"""
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
    1. mile > 30
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
    return item.get('control')


def price(item, logger):
    p = item.get('price')
    p = Decimal(p)
    if p <= 0 or p > 1000:
        return False
    average_price = get_average_price(
        item['brand_slug'], item['model_slug'], item['year'], item['volume'])
    if average_price:
        year = datetime.now().year
        # a = 2*(v_avg_price*v_count+v_price)/(v_count+1)
        # b = v_avg_price*v_count+v_price)/(v_count+1)/2
        a = average_price.avg_price * average_price.units + p
        a = a / (average_price.units + 1)
        a = 2 * a
        b = a / 2
        if average_price.avg_price_bn:
            if year - average_price.year == 0:
                return p <= average_price.avg_price_bn * Decimal('1.2')
            elif year - average_price.year == 1:
                return p <= average_price.avg_price_bn * Decimal('1.1')
            elif year - average_price.year > 1:
                return p < average_price.avg_price_bn
        else:
            return b <= p <= a
    return True


def brand_slug(item, logger):
    return item.get('brand_slug')


def model_slug(item, logger):
    return item.get('model_slug')


def phone(item, logger):
    tel = item.get('phone')
    if tel and tel.startswith('http'):
        match = ConvertPhonePic2Num(tel).find_possible_num()[0]
        tel = match[0]
        if match[1] == 0.99 and tel:
            item['phone'] = tel
        else:
            return False
    return tel
    # return phone_validate(tel)


def phone_validate(phone):
    u""" 判断电话号码是否有效 """
    if (phone[:2] in ('13', '15', '18') or phone[:3] == '147') and len(phone) in (10, 11):
        return True
    else:
        return False


def maintenance_desc(item, logger):
    value = item.get('maintenance_desc')
    if value:
        if '-' in value:
            value = u'不详'
    else:
        value = item.get('maintenance_record') and u'有4S店保养' or u'无4S店保养'
    return value


def city(item, logger):
    return item.get('province') and item.get('city')


def imgurls(item, logger):
    """
    没有图片不行，但可以没有缩略图，这时使用第一张图片
    nopic： 图片里不能有默认图片
    """
    imgurls = item.get('imgurls')
    item['imgurls'] = souche.imgurls(imgurls)
    return imgurls and 'nopic' not in imgurls


# ==============================================================================
# 数据库操作
# ==============================================================================
def insert_to_carsource(item, session, logger):
    car_source = CarSource()
    for attr in 'url title brand_slug model_slug mile year month control \
        city price volume color thumbnail phone domain source_type province'.split():
        setattr(car_source, attr, item[attr])
    car_source.pub_time = item['time'] or item['created_on']
    car_source.model_detail_slug = item['detail_model']
    car_source.mile = item['mile']
    car_source.status = 'sale'

    try:
        session.add(car_source)
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.error(u'Dup car_source {0}'.format(car_source.url))
        car_source = session.query(CarSource).filter_by(url=car_source.url).first()
    except Exception as e:
        # session.rollback()
        # raise
        # pdb.set_trace()
        logger.error(u'Unknown {0}:\n{1}'.format(car_source.url, unicode(e)))
        return
    else:
        logger.info(u'Saved car_source {0}'.format(car_source.url))
    insert_to_cardetailInfo(item, car_source, session, logger)
    insert_to_carimage(item, car_source, session, logger)
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
    try:
        # with session.begin_nested():
            # session.merge(car_detail_info)
        session.add(car_detail_info)
        # session.commit()
    except IntegrityError:
        session.rollback()
        msg = u'Dup car_detail_info for car_source: {0}'.format(car_source.id)
        logger.error(msg)
    except Exception as e:
        logger.error(u'Failed {0}: \n{1}'.format(car_source.url, unicode(e)))
    else:
        logger.info(u'Add car_detail_info: {0}'.format(car_detail_info.id))
    #return car_detail_info


def insert_to_carimage(item, car_source, session, logger):
    imgs = item['imgurls'].split()
    for img in imgs:
        car_image = CarImage()
        car_image.car = car_source
        car_image.image = img
        try:
            session.add(car_image)
            session.commit()
            logger.debug(u'Add CarImage {0}'.format(img))
        except IntegrityError:
            session.rollback()
            msg = u'Dup CarImage for car_source: {0}'.format(car_source.id)
            logger.error(msg)
        except Exception as e:
            logger.error(u'Failed {0}: \n{1}'.format(car_source.url, unicode(e)))
    #else:
    logger.info(u'Saved CarImages for car_source: {0}'.format(car_source.id))


#==============================================================================
# utils 函数
#==============================================================================

def upload_img(item, logger):
    thumbnail = item.get('thumbnail')
    if not thumbnail:
        item['thumbnail'] = thumbnail = item['imgurls'].split(' ')[0]
    if thumbnail:
        base_qiniu = 'http://gongpingjia.qiniudn.com/'
        if thumbnail.startswith(base_qiniu):
            return thumbnail
        logger.info(u'上传 thumbnail：{0}'.format(thumbnail))
        qiniu_url = upload_to_qiniu(thumbnail, QINIU_IMG_BUCKET)
        if qiniu_url:
            logger.info(u'上传 thumbnail成功：{0}'.format(qiniu_url))
            item['thumbnail'] = thumbnail = base_qiniu + qiniu_url
        else:
            logger.info(u'上传 thumbnail失败：{0}'.format(thumbnail))
    else:
        logger.error(u'没有 thumbnail，原始 URL：{0}'.format(item['url']))
    return thumbnail


def upload_imgs(item, logger):
    imgurls = item['imgurls']
    base_qiniu = 'http://gongpingjia.qiniudn.com/'
    if imgurls and imgurls.startswith(base_qiniu):
        return imgurls
    imgurls = imgurls.split(' ')
    if not imgurls:
        return None
    urls = batch_upload_to_qiniu(imgurls, QINIU_IMG_BUCKET)
    _urls = []
    for url in urls:
        a_url = base_qiniu + url
        _urls.append(a_url)
    if _urls:
        item['thumbnail'] = _urls[0]
    item['imgurls'] = ' '.join(_urls)
