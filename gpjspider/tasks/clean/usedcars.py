# -*- coding: utf-8 -*-
"""
关于优质二手车清洗的任务
"""
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, Column
# from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from gpjspider.items import UsedCarItem
from gpjspider.models.product import CarSource, CarDetailInfo, CarImage, Dealer
from gpjspider.models import UsedCar, TradeCar
from gpjspider.services.cars import get_gpj_category
from gpjspider.services.cars import get_gpj_detail_model
from gpjspider.services.cars import get_average_price
# from gpjspider.services.city import get_gongpingjia_city

from gpjspider.utils.tracker import get_tracker
from gpjspider.tasks.utils import upload_to_qiniu, batch_upload_to_qiniu
from gpjspider.utils.misc import sorted_unique_list
from gpjspider.utils.constants import (
    QINIU_IMG_BUCKET,
    USE_CELERY_TO_SAVE_CARSOURCE,
)
from gpjspider.utils.phone_parser import ConvertPhonePic2Num
from gpjspider.utils import get_mysql_connect, get_mysql_cursor as get_cursor
from gpjspider.processors import souche
from gpjspider.utils.misc import filter_item_ids
from sqlalchemy import func
from threading import Thread, Lock

import threading
import re
try:
    import ipdb
except ImportError:
    import pdb as ipdb
from time import sleep
import requests
import json
from gpjspider.utils import get_redis_cluster
redis = get_redis_cluster()
Session = get_mysql_connect()

import logging

def get_task_logger(name='clean'):
    return logging.getLogger(name)

AUTO_PHONE = False
# 需要检查去重的产品表
DUP_CAR_CHECK_TYPES=(
    # TradeCar,
    CarSource,
)
# 需要检查去重的产品表字段（如果表里没有对应的字段则会给出对应的)
DUP_CAR_CHECK_FIELDS=(
    'brand_slug',
    'model_slug',
    'city',
    'year',
    'mile',
    'price',
    'phone',
)
from gpjspider.utils.constants import (
    REDIS_DUP_SIG_KEY,
    REDIS_DUP_STAT_KEY,
    REDIS_DUP_CHECKED_KEY,
    CLEAN_ITEM_HOUR_LIMIT, 
    CLEAN_STATUS,
    CLEAN_MIN_ID,
) 

class CleanException(Exception):
    pass

class MatchDealerException(Exception):
    pass


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



def log(msg, *args):
    logging.debug(u'%s%s' % (unicode(msg), u','.join([unicode(arg) for arg in args])))
    print str(datetime.now())[11:19], msg,
    for arg in args:
        print arg,
    print ''


@app.task(name="update_sell_dealer", bind=True, base=GPJSpiderTask)
def update_sell_dealer(self, item_id):
    session = Session()
    item = session.query(CarSource).filter_by(id=item_id).first().__dict__
    try:
        item.update(session.query(CarDetailInfo).filter_by(car_id=item_id).first().__dict__)
    except:
        pass
    dealer_id = None
    msg = ''
    try:
        dealer_id = match_dealer(item, reraise=True)
    except Exception as e:
        msg=e.message

    if dealer_id:
        session.query(CarSource).filter_by(id=item_id).update(dict(dealer_id=dealer_id), synchronize_session=False)
        log('[update_sell_dealers]updated', item_id,  dealer_id)
    else:
        dealer_id = 0
        if not msg:
            msg='not_enough_infomation'
        log('[update_sell_dealers]fail', item_id, msg)
    session.close()

def test_dup_car():
    session = Session()
    items=TradeCar.mock_dup_car(session)
    for item in items:
        clean_item(item['id'])
    session.close()


@app.task(name="update_dup_car", bind=True, base=GPJSpiderTask)
def update_dup_car(self, klass_name, item_id):
    if redis.sismember(REDIS_DUP_CHECKED_KEY, item_id):
        log('[update_dup_car]checked', item_id)
        return
    redis.sadd(REDIS_DUP_CHECKED_KEY, item_id)
    found=False
    for klass in DUP_CAR_CHECK_TYPES:
        if klass_name==klass.__name__:
            found=True
            break
    if not found:
        raise Exception('Unkown dup car type')
    session = Session()
    try:
        row = session.query(klass).filter_by(id=item_id).first()
        if row is None:
            raise Exception('%s<%s> not exists' % (klass.__name__, item_id))
        item=row.__dict__
        old_item_ids = get_dup_car_items(item, klass_name)
        old_item_ids = filter_item_ids(old_item_ids, klass_name)
        if old_item_ids:
            klass.mark_duplicate(session, item_id, old_item_ids)
            log('[update_dup_car]duplicate', item_id, ','.join(map(str, old_item_ids)))
        else:
            log('[update_dup_car]pass', item_id)
    except Exception as e:
        raise
    finally:
        session.close()

@app.task(name="update_dup_cars", bind=True, base=GPJSpiderTask)
def update_dup_cars(self, step=5, limit=None, async=False):
    log('update_dup_cars')
    session = Session()
    cursor = get_cursor(session)
    for klass in DUP_CAR_CHECK_TYPES:
        log('checking type', klass.__name__)
        base_query = session.query(klass.id)
        min_id = base_query.order_by(klass.id.asc()).limit(1).scalar()
        max_id = base_query.order_by(klass.id.desc()).limit(1).scalar()
        # step = 5
        log('min_id', min_id)
        log('max_id', max_id)
        i=0
        for row in base_query.filter(klass.id>=min_id, klass.id<=max_id).order_by(klass.id.asc()).yield_per(step):
            # log('processing ', row.id)
            item_id = str(row.id)
            if async:
                update_dup_car.delay(klass.__name__, item_id)
            else:
                update_dup_car(klass.__name__, item_id)
            i+=1
            if limit and i>limit:
                break
        log('checked type', klass.__name__)
    log('done, close connection')
    session.close()


@app.task(name="update_sell_dealers", bind=True, base=GPJSpiderTask)
def update_sell_dealers(self, step=5, limit=None, async=False):
    log('update sell dealers')
    session = Session()
    cursor = get_cursor(session)
    base_query = session.query(CarSource.id)
    min_id = base_query.order_by(CarSource.pub_time.asc()).limit(1).scalar()
    max_id = base_query.order_by(CarSource.pub_time.desc()).limit(1).scalar()
    # step = 5
    log('min_id', min_id)
    log('max_id', max_id)
    i=0
    for row in base_query.filter(CarSource.id>=min_id, CarSource.id<=max_id, CarSource.dealer_id==0).order_by(CarSource.id.asc()).yield_per(step):
        # log('processing ', row.id)
        item_id = str(row.id)
        if async:
            update_sell_dealer.delay(item_id)
        else:
            update_sell_dealer(item_id)
        i+=1
        if limit and i>limit:
            break
    log('done, close connection')
    session.close()

@app.task(name="clean_domain", bind=True, base=GPJSpiderTask)
# def clean_domain(self, domain=None, sync=True, amount=50, per_item=10):
def clean_domain(self, domain=None, sync=False, amount=50, per_item=10):
    log('Starting..')
    session = Session()
    cursor = get_cursor(session)
    domains = domain and [domain] or [
        'xin.com',
        'haoche.ganji.com',
        '99haoche.com',
        'ygche.com.cn',
        'haoche51.com',
        'renrenche.com',
        'souche.com',
        'youche.com',

        '58.com',
        'ganji.com',
        'baixing.com',
        'taoche.com',
        '51auto.com',
        '273.cn',
        'cn2che.com',
        'used.xcar.com.cn',
        'iautos.cn',
        '2sc.sohu.com',

        'hx2car.com',
        'che168.com',
        'cheshi.com',

        'c.cheyipai.com',
    ]
    # created_on>=curdate()  between '2015-05-1' and '2015-05-10' '2015-05-10' and '2015-05-20'  and id>17549018
    # subdate(curdate(), interval 8 day)
    # update = "update open_product_source set status='C' where created_on > '2015-06-18' and source_id=1 \
    # update = "update open_product_source set status='C' where created_on>=curdate() and source_id=1 \ a.domain='ygche.com.cn'
    # where created_on between '2015-6-26' and '2015-7-2' and source_id=1 \
        # created_on>=subdate(now(), interval 1 hour) \
    update = "update open_product_source a, car_source b set a.status='C' where \
        created_on>=curdate() \
        and source_id=1 and a.url=b.url and a.status in ('I');"
    # if sync:
    #     cursor.execute(update.format("','".join(domains)))
    status = 'Y'
    if CLEAN_STATUS:
        status = CLEAN_STATUS
    # status = ' imgurls' # control imgurls
    # status = 'I'
    # status = '-model_slug'
    # status = '_'
    # status = '_t'
    # status = 'E' # E N P C
    # status = 'C'
    statuss = status.split(',')

    min_id = CLEAN_MIN_ID
    if not min_id:
        start_date = datetime.today()
        if CLEAN_ITEM_HOUR_LIMIT>=24:
            start_date -= timedelta(days=CLEAN_ITEM_HOUR_LIMIT/24)
        start_time = str(start_date)[:10]
        # print start_time
        sql = session.query(UsedCar.id).filter(
            UsedCar.created_on >= start_time,
            # UsedCar.created_on < str(datetime.now())[:10],
            # UsedCar.created_on < '2015-07-23',
            # UsedCar.created_on < '2015-07-27',
            UsedCar.domain.in_(domains),
            # UsedCar.created_on >= '2015-07-9',
            # UsedCar.created_on >= '2015-07-6',
            # UsedCar.status.in_(['N', 'Y']),
            #UsedCar.status.in_([status, 'I']),
            UsedCar.status.in_(statuss),
           # UsedCar.id>26630143,
            #UsedCar.id>26836404,
            # UsedCar.status.in_([status, 'Y', 'I']),
        ).filter_by(source=1)
        #ipdb.set_trace()
        #.order_by(UsedCar.id.asc())
        try:
            min_id = sql.first().id
        except Exception as e:
            session.close()
            log('Done,missing min_id', e.message)
            return
    # created_on>curdate()
    # created_on between subdate(curdate(), interval 1 day) and curdate() "2015-07-11" <"2015-07-12"
    # created_on>subdate(now(), interval 2 hour)
    # select = ('select %s(id) from open_product_source where created_on>subdate(now(), interval %d hour) and source_id=1 '
    #     # 'and status="%s" '
    #     'and domain in (\'%s\');'
    #     )
    try:
        # max_id = cursor.execute(select % ('max', CLEAN_ITEM_HOUR_LIMIT,
        #     #status,
        #     "','".join(domains)
        #     )).fetchone()[0]
        max_id = session.execute('select id from open_product_source order by id desc limit 1').fetchone()[0]
        if not max_id:
            raise Exception('max id is not created')
    except:
        session.close()
        log('no max id')
        return
    # min_id = 21711200 # 17547311 20052220 21252445
    # max_id = 22470882
    # min_id, max_id = 21588122, 21588667
    # min_id, max_id = 21861584, 21921761
    # min_id, max_id = 21203289, 21693372
    # min_id, max_id = 21403289, 21693372
    # min_id, max_id = 21693372, 21784860
    # min_id, max_id = 21876718, 21876719
    # min_id, max_id = 21877089, 21877090
    # min_id, max_id = 21877089, 22028667
    # min_id, max_id = 21889949, 22028667
    # min_id, max_id = 21289949, 21877089
    # min_id, max_id = 21877164, 21877165
    # min_id, max_id = 22857674, 22857684
    # min_id, max_id = 23628009, 23818197
    # min_id, max_id = 23627225, 23798031
    # min_id = 23778888
    # max_id = 23778889
    # id_range = 2000
    id_range = 5000
    # id_range = 10000
    # id_range = 20000
    # id_range = 50000
    # id_range = 500
    log('cleaning %d-%d, total %d items' % (min_id, max_id, max_id - min_id + 1))
    while min_id < max_id:
        mid = min_id + id_range
        if mid > max_id:
            mid = max_id
        clean(min_id, mid, domains, ','.join(statuss))
        min_id = mid
        # return
    log('Done')

WORKER = 40
WORKER = 10
WORKER = 5
WORKER = 3
# WORKER = 2
# WORKER = 20
WORKER = 0

# def inspect_reason(item, group, reason, detail=''):
#     session = Session()
#     from gpjspider.models.product import ReasonTrack
#     from datetime import datetime
#     track = ReasonTrack(item_id=item['id'], group=group, code=reason, detail=detail, created_at=datetime.now())
#     session.add(track)
#     session.commit()


def clean(min_id, max_id, domains=None, status='Y', session=None):
    # print min_id, max_id
    # base query
    # session = session or Session()
    log('cleaning %s-%s' % (min_id,max_id))
    # ipdb.set_trace()
    statuss = status.split(',')
    session = Session()
    try:
        domains = domains or []
        base_query = session.query(UsedCar).filter(
            UsedCar.id >= min_id,
            UsedCar.id <= max_id,
            UsedCar.source_type != 1,
        ).filter_by(
            source=1
        )
        if domains:
            base_query = base_query.filter(UsedCar.domain.in_(domains))
        #ipdb.set_trace()
        # mark status=I, processing
        wait_status = 'I'
        base_query.filter(
            UsedCar.status.in_(statuss)
        ).update(dict(status=wait_status), synchronize_session=False)
        # filter processing query
        q = base_query.filter_by(status=wait_status)
        # mark null field
        for field in 'city phone brand_slug model_slug year month volume mile price imgurls control title'.split():
            filts = [Column(field) == None, Column(field) == '']
            if field in 'price volume year month'.split():
                filts[1] = Column(field) == 0
                if field == 'month':
                    filts.append(Column(field) > 12)
            elif field == 'imgurls':
                filts.append(~Column(field).like('http%'))
            # elif field in 'control'.split():
            #     filts.pop()
            q.filter(or_(*filts)).update(dict(status=' %s' % field), synchronize_session=False)
        # mark invalid cars
        # 1. match bmd
        pass

        # push to car_source
        # filter good car_source
        # log('filter good car_source..')
        bq = session.query(UsedCar.id).filter(
            UsedCar.id >= min_id,
            UsedCar.id <= max_id,
            UsedCar.source_type != 1
        ).filter_by(
            source=1
        )
        # iq = bq.filter_by(status=wait_status).filter(
            # UsedCar.domain.in_(domains), UsedCar.control != None)
        iq = bq.filter_by(
            status=wait_status
        ).filter(
            UsedCar.control != None
        )
        if domains:
            iq = iq.filter(UsedCar.domain.in_(domains))
        good_cars = iq.filter(
            ~UsedCar.phone.like('http%'),
            UsedCar.year > 2007,
            UsedCar.mile < 30
        )
        pool_run(good_cars, clean_usedcar)

        # filter normal car_source
        # TODO: push all
        # log('filter normal car_source..')
        normal_cars = iq.filter(
                UsedCar.year > 1970,
                UsedCar.mile < 200
        )

        pool_run(normal_cars, clean_normal_car)

        log('marking status in N,I to _ in UsedCar')
        end_status = '_'
        # mark left cars
        marked_cnt = base_query.filter(UsedCar.status.in_(['N', 'I'])).update(dict(status=end_status), synchronize_session=False)
        log('%d items marked as status _' % marked_cnt)
        # push to sell_car
        # log('push to sell_car..')
        trade_cars = bq.filter_by(
            source_type=4,
            checker_runtime=1
        ).filter(
            # UsedCar.domain.in_(domains),
            UsedCar.status.in_([end_status, ' control', ' imgurls', ' mile', ' title', '-price']),
            UsedCar.city.in_([u'\u5317\u4eac', u'\u6210\u90fd', u'\u5357\u4eac']),
            or_(UsedCar.phone.like('1%'), UsedCar.phone.like('http://%')),
            UsedCar.year > 1970,
            UsedCar.mile < 200
        )
        if domains:
            trade_cars = trade_cars.filter(UsedCar.domain.in_(domains))
        pool_run(trade_cars, clean_trade_car)
    except Exception as e:
        get_task_logger().error('clean error', exc_info=True)
    finally:
        session.close()
        log('clean done')


def match_dealer(item, reraise=False):
    '''
    根据数据的车商名字和城市来匹配到具体的raw_sell_dealer然后更新数据的这条信息
    '''
    try:
        if not (item['city'] and item['company_name']):
            return None
    except:
        return None
    from gpjspider.models.usedcars import RawSellDealer
    session = Session()
    ctx= dict(company_name=item['company_name'])
    tags={
        'city':item['city'],
        'domain':item['domain'],
        'operation':'MatchDealer',
    }
    dealer_id = None
    try:
        query = session.query(RawSellDealer.dealer_id).filter(
            RawSellDealer.city==item['city'],
            RawSellDealer.domain==item['domain'],
            or_(
                RawSellDealer.company_name==item['company_name'],
                RawSellDealer.company_name=="'%s'" % item['company_name']
            )
        )
        cnt = query.count()

        if cnt<1:
            raise MatchDealerException('NoMatchedRawSeller')
        elif cnt>1:
            ctx['count']=cnt
            raise MatchDealerException('DuplicateRawSeller')
        # when cnt==1 we go on
        dealer_id = query.scalar()
        if not dealer_id:
            raise MatchDealerException('EmptyRawSeller')
    except MatchDealerException as e:
        try:
            get_tracker().captureMessage(e.message, extra=ctx, tags=tags)
        except:pass
        if reraise:
            raise e
        print e.message
        for k, v in ctx.items():
            print k, v
        for k, v in tags.items():
            print k, v
    except Exception as e:
        try:
            get_tracker().captureException(extra=ctx, tags=tags)
        except:pass
        if reraise:
            raise e
        print e.message
    finally:
        session.close()
    if not reraise:
        print dealer_id
    return dealer_id



def clean_item(item_id):
    session=Session()
    query = session.query(UsedCar).filter_by(id=item_id)
    print 'try to clean item', item_id
    items=[]
    for item in query:
        items.append(item.__dict__)
    session.close()
    clean_normal_car(items)
    #clean_trade_car(items)
    #clean_usedcar(items)


def match_item_dealer(item_id):
    session=Session()
    query = session.query(UsedCar).filter_by(id=item_id)
    print 'try to match delaer for item', item_id
    items=[]
    for item in query:
        items.append(item.__dict__)
        ditem = item.__dict__
        print ditem['id'], ditem['city'], ditem['company_name'], ditem['domain']
        ditem['dealer_id']=match_dealer(ditem)
    session.close()
    print 'done'

def pool_run(query, meth, index=0, psize=10, cls=UsedCar):
    remain = query.count()
    log('pool_run %s, query item count %s' % (meth.__name__, remain))
    if not remain:
        log('empty query, return')
        return
    # psize = 30
    # psize = 60
    # psize = 100
    amount = (remain / psize) + 1
    global WORKER
    items = []
    for item in query.yield_per(psize):
        items.append(str(item.id))
        if index % psize == 0:
            if WORKER:
                if index % 500 == 0:
                    log(amount, '%s - %s' % (min(items), max(items)))
                async_clean(meth, items, cls)
            else:
                # print 'sync cleaning'
                log(amount, '%s - %s' % (min(items), max(items)))
                sync_clean(meth, items, cls)
            amount -= 1
            items = []
        index += 1
    # print 'remains cleaning'
    if items:
        log(amount, '%s - %s' % (min(items), max(items)))
        if WORKER:
            async_clean(meth, items, cls)
        else:
            sync_clean(meth, items, cls)
        # async_clean(meth, items)
        # sync_clean(meth, items)


def push_trade_car(item, sid, session):
    old_trade_car_item_ids = get_dup_car_items(item, 'TradeCar', is_new=True)
    if old_trade_car_item_ids and TradeCar.last_dup_item_is_alive(session, old_trade_car_item_ids):
        # 重复车源，旧的车源还在存活期类，则不进入
        log('duplicated and old item is alive, no push_trade_car',sid)
        return False, 'old duplicated item is alive, stop push trade_car'
    else:
        log('new item, do push_trade_car',sid)
    try:
        car = TradeCar.init(item)
        session.add(car)
        session.commit()
        session.query(UsedCar).filter_by(id=sid).update(dict(
            checker_runtime_id=0,
                # status='_t'
        ), synchronize_session=False)
        update_dup_car_items(item, 'TradeCar', car.id)
        return True, 'ok'
    except IntegrityError:
        session.rollback()
        return False, 'IntegrityError'
    except Exception as e:
        # raise
        print e, sid
        return False, e.message



def clean_trade_car(items, do_not_push=False):
    for item in items:
        session = Session()
        detail = ''
        ctx = {}
        tags={'domain':item['domain'], }
        for f in 'title,dmodel,model_slug,brand_slug'.split(','):
            ctx['origin_%s' % f] = unicode(item.get(f, None))
        sid = str(item['id'])
        # print 'clean_trade_car', sid
        try:
            item_is_trade_car, codes = is_trade_car(item, True)
            if not item_is_trade_car:
                detail = ','.join(codes)
                del codes
                raise CleanException('is_not_trade_car')

            match_bmd(item, session=session)
            if not (item['brand_slug'] and item['model_slug']):
                tags['Car_Model']=ctx['origin_model_slug']
                tags['Car_Brand']=ctx['origin_brand_slug']
                raise CleanException('empty_brand_or_model')
            elif type(item['model_slug']) in (float, long, int):
                tags['Car_Model']=ctx['origin_model_slug']
                tags['Car_Brand']=ctx['origin_brand_slug']
                detail=u'{} - {}'.format(item['brand_slug'], item['model_slug'])
                raise CleanException('duplicat_brand_or_model')
            if not do_not_push:
                pushed, push_error = push_trade_car(item, sid, session)
                if not pushed:
                    raise CleanException(push_error)
            else:
                print 'clean_trade_car pass', sid, item['phone']
                print ctx['origin_brand_slug'], ctx['origin_model_slug'] , '==>', item['brand_slug'], item['model_slug']
        except CleanException as e:
            code = e.message
            for f in 'domain,id,volume,phone,city,source_type,model_slug,brand_slug,url'.split(','):
                ctx[f] = item.get(f, None)
            if detail:
                ctx['detail']=detail
            del f
            del detail
            try:
                get_tracker().captureMessage(e.message, extra=ctx, tags=tags)
            except:
                get_task_logger().error('clean error %s' % sid, exc_info=True)
            # if do_not_push:
            #     ipdb.set_trace()
            # get_task_logger('clean_trade_car').error('clean fail for %s' % code, exc_info=True, extra=ctx)

            if 0:# 暂时使用sentry记录，不在保存在本地数据库
                from gpjspider.models.product import ReasonTrack
                ctx = json.dumps({k:unicode(v) for k,v in ctx.items()}, ensure_ascii=False)
                track = ReasonTrack(item_id=item['id'], domain=item['domain'], code=code, detail=detail, ctx=ctx, created_at=datetime.now())
                session.add(track)
                session.commit()
            # print 'new clean_trade_car on'
        except Exception as e:
            try:
                get_tracker().captureException()
            except:
                get_task_logger().error('uncaught error %s' % sid, exc_info=True)
        finally:
            session.close()
    log('clean_trad_car done')


@async
def async_clean(func, items, *args, **kwargs):
    sync_clean(func, items, *args, **kwargs)
    sleep(0.15)


def sync_clean(func, items, *args, **kwargs):
    log('sync_clean %s %s items min:%s max:%s' % (func.__name__, len(items), min(items), max(items)))
    global WORKER
    WORKER -= 1
    cls = args[0]
    if cls and isinstance(items[0], basestring):
        ids = items
        items = []
        session = Session()
        for item in session.query(cls).filter(cls.id.in_(ids)).yield_per(10):
            items.append({k:v for k,v in item.__dict__.iteritems() if not k.startswith('_')})
        session.close()
    func(items, **kwargs)
    # get_cursor().execute('update open_product_source set checker_runtime_id=0 \
    #     where id in (%s);' % ','.join(ids))
    WORKER += 1
    log('sync_clean done')


def update_item(item, **kwargs):
    for k, v in kwargs.items():
        if not item.get(k):
            item[k] = v

def first_mobile(s):
    if s.startswith('http://'):
        return s
    import re
    try:
        return re.findall(r'\b1\d{10}\b', s)[0]
    except:
        return s

def is_trade_car(item, throw_reason=False):
    item['phone'] = first_mobile(item['phone'])
    valid_source_types = (4, 'cpersonal', 'personal')
    criteria = (
        (item['source_type'] in valid_source_types, 'invalid_source_type',),
        (item['city'] in [u'\u5317\u4eac', u'\u6210\u90fd', u'\u5357\u4eac'], 'invalid_city'),
        (item['volume'], 'empty_volume',),
        (item['phone'], 'empty_phone',),
        (len(item['phone']) == 11 or item['phone'].startswith('http://'), 'invalid_phone',),
    )

    can_go = True
    errors = []
    for is_valid, code in criteria:
        if not is_valid:
            can_go = False
            errors.append(code)

    if not can_go:
        if throw_reason:
            return False, errors
        return False

    global AUTO_PHONE
    tel = item['phone']
    if item['phone'].startswith('http'):
        if '#' in tel:
            if AUTO_PHONE and tel.endswith('#0.99'):
                tel = first_mobile(tel.split('#')[1])
        else:
            # added by y10n
            # 识别手机号码的代码中出现错误的时候如果有错误没有被处理的时候我们应该在此捕获，不影响后续的清理
            try:
                tel_info = ConvertPhonePic2Num(tel).find_possible_num()
                tel += '#%s#%s' % tel_info
                # print item['id'], tel
            except Exception as e:
                get_task_logger('is_trade_car').error(e, exc_info=True)
                return False, ['captcha error', tel, e.message or str(e)]

        item['phone'] = tel
    if throw_reason:
        return True, []
    return True



def is_dup_psid(psid):
    clean_count = redis.zincrby('clean_psid', psid)
    if clean_count > 3:
        print psid, clean_count
    return clean_count > 1

def make_item_sig(item):
    from gpjspider.utils.common import _md5
    if not item.has_key('brand_slug'):
        item['brand_slug'] = item['brand']
    if not item.has_key('model_slug'):
        item['model_slug'] = item['model']
    car_info = u'#'.join([unicode(item[field]) for field in DUP_CAR_CHECK_FIELDS])
    sig = _md5(car_info.encode('utf-8'))
    return car_info, sig

def update_dup_car_items(item, klass_name, klass_id):
    try:
        detail, sig = make_item_sig(item)
        rk = REDIS_DUP_SIG_KEY % sig
        item_id = '%s:%s' % (klass_name,klass_id)
        if redis.exists(rk) and redis.sismember(rk, item_id):
            redis.zincrby(REDIS_DUP_STAT_KEY, sig)
        redis.sadd(rk, item_id)
    except Exception as e:
        get_task_logger().error('during update dup_car_items %s:%s, item:' % (klass_name, klass_id, item['id']), exc_info=True)

def get_dup_car_items(item, klass_name='UsedCar', is_new=False):
    try:
        detail, sig = make_item_sig(item)
        rk = REDIS_DUP_SIG_KEY % sig
        if not is_new:
            item_id = '%s:%s' % (klass_name, item['id'])
            if redis.exists(rk) and redis.sismember(rk, item_id):
                redis.zincrby(REDIS_DUP_STAT_KEY, sig)
            else:
                redis.sadd(rk, item_id)
            item_ids = [i for i in redis.smembers(rk)  if not i==item_id]
        else:
            item_ids = redis.smembers(rk)
        item_ids = [x[1] for x in [i.split(':')  for i in item_ids] if x[0]==klass_name]
        return item_ids
    except Exception as e:
        get_task_logger().error('get dup_items for %s fail' % item['id'], exc_info=True)
        return []

def is_dup_car_redis2(item):
    detail, sig = make_item_sig(item)
    rk = 'dupcar_%s' % sig
    found= False
    if redis.exists(rk) and redis.sismember(rk, item['id']):
        redis.zincrby('dupcar_stat', sig)
        found=True
    else:
        redis.sadd(rk, item['id'])
    return found
#
# def is_dup_car_mysql(item):
#     from gpjspider.models.usedcars import CarFingerprint
#     session = Session()
#     detail, sig = make_item_sig(item)
#     found = False
#     if 1:
#     # try:
#         cfp = session.query(CarFingerprint).filter_by(sig=sig).first()
#         if cfp is not None:
#             session.query(CarFingerprint).filter_by(id=cfp.id).update(dict(cnt=cfp.cnt+1), synchronize_session=False)
#             found=True
#     # except Exception as e:
#         else:
#             get_tracker().captureException()
#             cfp = CarFingerprint(sig=sig, detail=detail, cnt=1)
#             session.add(cfp)
#     session.commit()
#     return found
#

def is_dup_car_redis(item):
    '''
    1. get car_hash
    2. if in cur_* set
    3.  add car_hash in cur_date set,
        # had dur_key set: [cur_date, cur_week, cur_month, cur_year] #, last_year
        had clean_psid zcard: [psid, psid, ...]
        had dur_key set: [cur_date, cur_week, cur_month, cur_year] #, last_year
        update dur_hset: {cur_date, cur_week, cur_month, cur_year}
        add %(cur_date)s+car_hash list: [ps_id, ps_id, ...]
    '''
    # time = item['time'] or item['created_on']
    # check ps id
    psid = item['id']
    check_psid = False
    if is_dup_psid(psid) and check_psid:
        return True
    time = datetime.today()
    cur_date = str(time)[:10]
    # Y-m-d
    # week_num = time.isocalendar()[1]
    # cur_week = '%s_%s' % (time.year, week_num)
    # cur_month = cur_date[:7]
    # cur_year = time.year
    # last_year = time.year - 1

    car_info, car_md5 = make_item_sig(item)
    # keys = [cur_date, cur_week, cur_month, cur_year] #, last_year
    # @todo update dur_keys, do not make it fat

    keys = redis.lrange('dur_keys', 0, -1)
    dur_key = None
    for key in keys:
        if redis.sismember(key, car_md5):
            dur_key = key
            break

    # add car md5 for new car
    if not dur_key:
        dur_key = keys[0]
        redis.sadd(cur_date, car_md5)

    info_key = 'info_' + dur_key
    if not redis.hsetnx(info_key, car_md5, psid):
        # record dup car info
        old = redis.hmget(info_key, car_md5)
        redis.hsetnx(info_key, car_md5, '%s %s' % (old, psid))
        redis.zincrby('stats_dup_car', car_md5)
        return True

def is_dup_car(item):
    return is_dup_car_redis2(item)
    # return is_dup_car_mysql(item)


def clean_normal_car(items):
    funcs = [title, city, price, model_slug, brand_slug, phone, month, imgurls, maintenance_desc]
    clean_usedcar(items, False, funcs)
    log('clean_normal_car done')

@app.task(name="save_to_car_source", bind=True, base=GPJSpiderTask)
def save_to_car_source(self, item, is_good=True):
    logger = get_task_logger()
    sid = str(item['id'])
    session = Session()
    if AUTO_PHONE:
        tel = re.findall('^http.+#(\d+)#0.99$', item['phone'])
        if tel:
            item['phone'] = tel[0]
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
    # elif 'c.cheyipai.com' == domain:
    #    update_item(item,
    #        company_name=u'车易拍客服', company_url='http://c.cheyipai.com',
    #        contact=u'车易拍客服', phone='400-733-6622')
    item['is_certifield_car'] = is_good and item['is_certifield_car']
    # 业务判断通过，后续处理
    upload_img(item, logger)
    # upload_imgs(item, logger)
    # 保存到产品表

    try:
        car_source = insert_to_carsource(item, session, logger)
        s=''
        if not car_source:
            logger.error(u'插入CarSource时失败:source.id:{0}'.format(sid))
            s = 'S'
        else:
            logger.error(u'清理source.id={0}成功'.format(sid))
            s = 'C'
        session.query(UsedCar).filter_by(id=sid).update(dict(status=s), synchronize_session=False)
    except:
        get_task_logger().error('save carsource fail', exc_info=True)
    finally:
        session.close()

@app.task(name="clean_usedcar", bind=True, base=GPJSpiderTask)
def clean_usedcar(self, items, is_good=True, funcs=None, *args, **kwargs):
    logger = get_task_logger('clean_usedcar')
    if not isinstance(items, list):
        items = [items]
    logger.debug(u'清理数据,长度:{0}'.format(len(items)))
    status = {
        'C': [],
        'P': [],
        'E': [],
        'S': [],
        'T': [],
    }
    global AUTO_PHONE
    for item in items:
        if isinstance(item, UsedCarItem):
            item = item._values
            continue
        session = Session()
        sid = str(item['id'])
        s=''
        try:
            item = preprocess_item(item, session, logger)
            # preprocess_item(item, session, logger)
            flag = is_normalized(item, logger, funcs)
            if flag is not True:
                logger.warning(u'source.id: {0} 不符合规则要求'.format(sid))
                log('flag not match',sid)
                if sid:
                    key = flag if isinstance(flag, basestring) else 'P'
                    if key not in status:
                        status[key] = []
                    status[key].append(sid)
                continue

            # 20150815, 逻辑改变，如果重复，将旧的记录标为下线，新的上线
            # if is_dup_car(item):
            #     status['T'].append(sid)
            #     print 'IS_DUP_CAR'
            #     get_tracker().captureMessage('IS_DUP_CAR', extra=item)
            #     continue
            # old_item_ids = get_dup_car_items(item)
            # if old_item_ids:
            #     status['T'].append(sid)
            #     log('IS_DUP_CAR', old_item_ids ,sid)
            #     get_tracker().captureMessage('IS_DUP_CAR', extra=item)
            item_is_trade_car,errors=is_trade_car(item, True)
            if item_is_trade_car:
                    push_trade_car(item, sid, session)
            else:
                log('is_trade_car, false', errors,sid)

            session.query(UsedCar).filter_by(id=sid).update(dict(status='c'), synchronize_session=False)
            item.pop('_sa_instance_state', '')
            if USE_CELERY_TO_SAVE_CARSOURCE:
                log('delay %s to celery to insert carsource' % sid)
                from gpjspider.tasks.clean import save_to_car_source as save_to_car_source_task
                save_to_car_source_task.delay(item, is_good)
            else:
                save_to_car_source(item, is_good)
        except Exception as e:
            get_task_logger().error('clean used_car error %s' % sid, exc_info=True)
            #ipdb.set_trace()
            #raise e
            s = 'E'
        if sid and s:
            status[s].append(sid)
        session.close()
    session=Session()
    for k, v in status.items():
        if v:
            log('marking %d item(s): %s as status %s' % (len(v), ','.join(v), k))
            session.execute('update open_product_source set status="%s" where id in (%s);' % (k, ','.join(v)))
    session.close()

    log('clean_used_car done')




def get_province_by_city(city, session=None):
    # redis.hmget('city', city)
    need_close=False
    if not session:
        session=Session()
        need_close=True
    res = session.execute('SELECT b.name FROM open_city a, open_city b WHERE a.name="%s" and a.parent=b.id;' % city).fetchone()
    if need_close:
        session.close()
    return res[0] if res else None


def preprocess_item(item, session, logger):
    # todo: 将 city 进行匹配
    if item.get('city'):
        # add cache for c p
        item['city'] = item['city'].strip(u' 市')
        province = get_province_by_city(item['city'], session)
        if province:
            item['province'] = province
        else:
            item['province'] = None
            return item
    else:
        return item

    domain = item['domain']
    # if domain in ['58.com']:
    #     if item['source_type'] in (2, 3) and not item['is_certifield_car']:
    #         item['is_certifield_car'] = True

    if item['source_type'] == 2:
        item['source_type'] = 'dealer'
    elif item['source_type'] == 3:
        item['source_type'] = 'cpo'
    elif item['source_type'] == 4:
        if item['is_certifield_car'] and domain in 'haoche.ganji.com renrenche.com haoche51.com'.split():
            item['source_type'] = 'cpersonal'
        else:
            item['source_type'] = 'personal'
    elif item['source_type'] == 5:
        item['source_type'] = 'odealer'

    # handle haoche's price_bn += price if st=2(old solution)
    if 'haoche.ganji.com' == domain and item['source_type'] == 'dealer' and item['price'] and item['price_bn']:
        item['price_bn'] += item['price']

    match_bmd(item, domain, session)
    return item


def match_bmd(item, domain=None, session=None):
    domain = domain or item['domain']
    gpj_category = get_gpj_category(
        item['brand_slug'], item['model_slug'], domain, session, item.get('model_url'))
    if not gpj_category:
        # logger.warning(u'No match model for: {0},{1},{2}'.format(
            # item['brand_slug'], item['model_slug'], domain))
        item['brand_slug'] = item['model_slug'] = None
    else:
        if isinstance(gpj_category, (int, long)):
            item['brand_slug'] = gpj_category
            item['model_slug'] = None
        else:
            item['brand_slug'] = gpj_category.parent
            item['model_slug'] = gpj_category.slug
            if domain != 'ygche.com.cn':
                gpj_detail_model = get_gpj_detail_model(
                    gpj_category, item['dmodel'], domain)
                if gpj_detail_model:
                    item['detail_model'] = gpj_detail_model.detail_model_slug
                    for attr in 'volume price_bn'.split():
                        if not item.get(attr):
                            value = getattr(gpj_detail_model, 'volume')
                            if value:
                                item[attr] = value
                    # if not item.get('volume') and gpj_detail_model.volume:
                    #     item['volume'] = gpj_detail_model.volume
                    # if not item.get('price_bn') and gpj_detail_model.price_bn:
                    #     item['price_bn'] = gpj_detail_model.price_bn
                # else:
                #     logger.warning(u'无法匹配到detail_model：{0},{1},{2}'.format(
                #         gpj_category.id, item['dmodel'], domain))


def is_normalized(item, logger, funcs=None):
    # global funcs
    funcs = funcs or [title, city, price, model_slug, brand_slug, phone, month, year, mile,
         # volume, control,
         imgurls, maintenance_desc]
    try:
        for func in funcs:
            if not func(item, logger):
                step = func.__name__
                error = '-%s' % step
                if step == 'model_slug':
                    bs = item['brand_slug']
                    if isinstance(bs, int):
                        error += str(bs)
                return error
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
        if 0 <= int(a_month) <= 12:
            return True
    except:
        pass
    item['month'] = 0  # None
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
    tel = item['phone']
    if tel and tel.startswith('http'):
        if '#' not in tel:
            phone_info = ConvertPhonePic2Num(tel).find_possible_num()
            item['phone'] += '#%s#%s' % phone_info
            # tel = item['phone']
            tel = phone_info[0]
    #     if tel.endswith('#0.99'):
    #         tel = tel.split('#')[1]
    # item['phone'] = tel
    if not re.match(u'^[ 0-9转～—－-]+$',tel):
        return False
    item['phone']=tel
    return tel

def phone2(item, logger):
    tel = item.get('phone')
    if tel and tel.startswith('http'):
        if AUTO_PHONE and tel.endswith('#0.99'):
            item['phone'] = tel = tel.split('#')[1]
            return tel
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
def add_extra_cols(car_source, gpj_index, eval_price):
    if gpj_index:
        car_source.eval_price = eval_price
        car_source.gpj_index = gpj_index
        car_source.process_status = 'S'

def insert_to_carsource(item, session, logger):
    car_source = CarSource()
    item['model_detail_slug'] = item.get('detail_model', '')
    for attr in 'url title brand_slug model_slug model_detail_slug mile year month control \
        city price volume color thumbnail phone domain source_type province'.split():
        setattr(car_source, attr, item[attr])
    car_source.pub_time = item['time'] or item['created_on']
    car_source.mile = item['mile']
    car_source.pid = item['id']
    # check is online/offline
    car_source.status = 'review' if 'Q' in item['status'] else 'sale'
    # add qs_tags, eval_price, gpj_index
    car_source.qs_tags = get_qs_tags(item.get('quality_service'))

    if 0:# debug only
        import time
        car_source.url='%s%s' %(car_source.url, time.time())
    # 根据数据的基本信息，从数据库中匹配商家信息
    try:
        car_source.dealer_id = match_dealer(item, reraise=True)
    except:
        pass
    if car_source.dealer_id:
        dealer_type = session.query(Dealer).filter(Dealer.id == car_source.dealer_id).first().category
        if dealer_type == 'c2c':
            car_source.source_type = 'cpersonal'
    eval_price = get_eval_price(item)
    if eval_price:
        gpj_index = get_gpj_index(item['price'], eval_price)
        add_extra_cols(car_source, gpj_index, eval_price)
    inserted=False
    try:
        # query = session.query(CarSource.id).filter_by(url=car_source.url)
        # if query.count():
        #     car_source.id = query.first().id
        #     session.merge(car_source)
        # else:
        old_car_source_item_ids = get_dup_car_items(item, 'CarSource', is_new=True)
        session.add(car_source)
        session.commit()
    except IntegrityError:
        log('duplicated')
        session.rollback()
        logger.error(u'Dup car_source {0}'.format(car_source.url))
        # session.query(CarSource.id).filter_by(url=car_source.url).update(dict(thumbnail=item['thumbnail']))
        car_source = session.query(CarSource).filter_by(url=car_source.url).first()
        if item['id']!=car_source.pid:
            car_source.pid = item['id']
            session.merge(car_source)
            session.commit()

        # car_source.id = session.query(CarSource.id).filter_by(url=car_source.url).first().id
        # session.merge(car_source)
        # session.commit()
    except Exception as e:
        session.rollback()
        print e,item['id']
        # raise
        logger.error(u'Unknown {0}:\n{1}'.format(car_source.url, unicode(e)))
        return
    else:
        inserted=True
        logger.info(u'Saved car_source {0}'.format(car_source.url))
    insert_to_cardetailInfo(item, car_source, session, logger)
    insert_to_carimage(item, car_source, session, logger)
    if inserted:
        try:
            update_dup_car_items(item, 'CarSource', car_source.id)
            if old_car_source_item_ids:
                # 重复的旧的车源标记为下线
                log('duplicated,mark old items as offline before insert_to_carsource',item['id'], car_source.id, old_car_source_item_ids)
                CarSource.mark_offline(session, old_car_source_item_ids, car_source.id)
        except:
            get_task_logger().exception('update_dup_car_items error, %s' % car_source.id)
            pass
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
    detail_id = 0
    logger.debug('saving detail info for car source %d' % car_source.id)
    try:
        session.add(car_detail_info)
        session.commit()
        detail_id = car_detail_info.id
    except IntegrityError:
        session.rollback()
        msg = u'Dup car_detail_info for car_source: {0}'.format(car_source.id)
        logger.error(msg)
    except Exception as e:
        logger.error(u'cdi Failed {0} {1}: \n{2}'.format(car_source.id, car_source.url, unicode(e)), exc_info=True)
    else:
        logger.info(u'Add car_detail_info: {0}'.format(detail_id))


def insert_to_carimage(item, car_source, session, logger):
    imgs = sorted_unique_list(item['imgurls'].split())
    # car_source.images.delete()
    old_image_count = len(car_source.images)
    if old_image_count:
        log('delete %d old images for car_source %s' % (old_image_count, car_source.id))
        session.query(CarImage).filter(CarImage.car==car_source).delete(synchronize_session=False)
    for img in imgs:
        car_image = CarImage(car=car_source, image=img)
        session.add(car_image)
    try:
        session.commit()
    except:
        session.rollback()
        get_task_logger().error('fail to add image for car_source %s, images:%s' % (car_source.id, item['imgurls']))
    else:
        log('added image for car_source %s, %d pics' % (car_source.id, len(imgs)))

    return
    car_images = car_source.images
    amount = len(car_images)
    index = 0
    img_cnt=0
    for img in imgs:
        if amount > index:
            car_image = car_images[index]
            index += 1
        else:
            car_image = CarImage(car=car_source)
        car_image.image = img
        try:
            # with session.begin_nested()
            session.merge(car_image)
            session.commit()
            logger.debug(u'Add CarImage {0}'.format(img))
        except IntegrityError:
            session.rollback()
            logger.error(u'Dup CarImage for car_source: {0}'.format(car_source.id))
        except Exception as e:
            session.rollback()
            logger.error(u'CarImage Fail {0}{1} {2}'.format(car_source.id, car_source.url,img), exc_info=True)
        else:
            img_cnt+=1
    logger.info(u'Saved {1}of{2} CarImages for car_source: {0}'.format(car_source.id, img_cnt, len(imgs)))


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


def get_qs_tags(quality_service):
    u'''
>>> get_qs_tags(u'无重大事故 15天包退')
u'\\u53ef\\u9000\\u6362 \\u65e0\\u5927\\u4e8b\\u6545'
>>> get_qs_tags(u'14天可退1年质保')
u'\\u8d28\\u4fdd \\u53ef\\u9000\\u6362'
>>> get_qs_tags(u'保证在 七天包退 延长质保')
u'\\u8d28\\u4fdd \\u53ef\\u9000\\u6362'
>>> get_qs_tags(u'绝非事故车 7天可退 真车实价')
u'\\u53ef\\u9000\\u6362 \\u65e0\\u5927\\u4e8b\\u6545'
>>> get_qs_tags(u'通过无事故承诺的好车，无重大事故，无火烧，无水淹如若不符，15天全额包退')
u'\\u53ef\\u9000\\u6362 \\u65e0\\u5927\\u4e8b\\u6545'
>>> get_qs_tags(u'此车享受45天或1800公里先行赔付承诺保障')
u'\\u5148\\u8d54\\u4ed8'
>>> get_qs_tags(u'14天包退，360天/20000公里保修')
u'\\u8d28\\u4fdd \\u53ef\\u9000\\u6362'
    '''
    if not quality_service:
        return ''
    tag_map = {
        u'质保': u'[联延质保修]{2}',
        u'可退换': u'[可包退换车款]{2,}',
        u'无大事故': u'[发现绝非无重大]{1,3}事故车?',
        u'先赔付': u'先行?赔付?',
    }
    keys = u'质保 可退换 无大事故 先赔付'.split()
    tags = set()
    tags = []
    # for k, v in tag_map.items():
    for k in keys:
        v = tag_map[k]
        if re.search(v, quality_service):
            # tags.add(k)
            tags.append(k)
    return ' '.join(list(tags))

num = 1
lock = Lock()
def update_eval_price_and_gpj_index(site):
    if site == '.':
        domains = [
            'xin.com',
            'haoche.ganji.com',
            '99haoche.com',
            'ygche.com.cn',
            'haoche51.com',
            'renrenche.com',
            'souche.com',
            'youche.com',

            '58.com',
            'ganji.com',
            'baixing.com',
            'taoche.com',
            '51auto.com',
            '273.cn',
            'cn2che.com',
            'used.xcar.com.cn',
            'iautos.cn',
            '2sc.sohu.com',

            'hx2car.com',
            'che168.com',
            'cheshi.com',

            'c.cheyipai.com',
        ]
    else:
        domains = [site]
    session = Session()
    min_id = session.query(func.min(CarSource.id)).filter(CarSource.status == 'sale').scalar()
    max_id = session.query(func.max(CarSource.id)).filter(CarSource.status == 'sale').scalar()
    session.close()
    while max_id >= min_id:
        session = Session()
        query = session.query(
            CarSource.id,
            CarSource.price,
            CarSource.source_type,
            CarSource.brand_slug,
            CarSource.model_slug,
            CarSource.model_detail_slug,
            CarSource.volume,
            CarSource.year,
            CarSource.month,
            CarSource.color,
            CarSource.mile,
            CarSource.city,
            CarSource.eval_price,
            CarSource.gpj_index
        ).filter(CarSource.id <= max_id, CarSource.id > max_id - 50, CarSource.status == 'sale', CarSource.domain.in_(domains))
        items = query.all()
        session.close()
        session = Session()
        thread_list = []
        for item in items:
            child_thread = Thread(
                target=deal_one_item,
                args=(session, item)
            )
            thread_list.append(child_thread)
            if len(thread_list) == 10:
                for child_thread in thread_list:
                    child_thread.start()
                for child_thread in thread_list:
                    child_thread.join()
                thread_list = []
        for child_thread in thread_list:
            child_thread.start()
        for child_thread in thread_list:
            child_thread.join()
        max_id = max_id - 50
        session.close()


def deal_one_item(session, item):
    global num
    global lock
    eval_price = None
    gpj_index = None
    item = item.__dict__
    eval_price = get_eval_price(item)
    lock.acquire()    # 加锁，防止变量值错乱
    if eval_price:
        gpj_index = get_gpj_index(item['price'], eval_price)
        if gpj_index:
            session.query(CarSource).filter(CarSource.id == item['id']).update(
                {CarSource.eval_price: eval_price,CarSource.gpj_index: gpj_index}
            )
    print '{0} id {1} eval_price {2: ^5}->{3: ^5} gpj_index {4: ^5}->{5: ^5}'.format(num, item['id'], item['eval_price'], eval_price, item['gpj_index'], gpj_index)
    num = num + 1
    lock.release()


def get_eval_price(item):
    u'''
curl 'http://www.gongpingjia.com/api/cars/evaluation/spider/?brand=audi&mile=15.00&model=audi-a6&d_model=60270_autotis&year=2002&month=6&city=%E6%B2%88%E9%98%B3&volume=2.8&intent=cpo'
>>> params = 'brand_slug=audi&mile=15.00&model_slug=audi-a6&model_detail_slug=60270_autotis&year=2002&month=6&city=沈阳&volume=2.8&color=&source_type=cpo'
>>> item = {}
>>> for p in params.split('&'):
...     k, v = p.split('=')
...     item[k] = v
>>> get_eval_price(item)
5.0
    '''
    st = item['source_type']
    intent = 'buy'
    if 'personal' in st:
        intent = 'private'
    elif 'cpo' == st:
        intent = st
    item['intent'] = intent
    api = ('http://www.gongpingjia.com/api/cars/evaluation/spider/?brand=%(brand_slug)s'
        '&model=%(model_slug)s&d_model=%(model_detail_slug)s&volume=%(volume)s&year=%(year)s'
        '&month=%(month)s&color=%(color)s&mile=%(mile)s&city=%(city)s&intent=%(intent)s')
    api %= item
    try:
        r = requests.get(api, timeout=20)
        if r and r.status_code == 200:
            data = r.text.strip()
            eval_price = json.loads(data)['deal_price']
            return decimal(int(eval_price) / 10000.0)
    except Exception as e:
        print e, item['id']

def decimal(value):
    return float('%.1f' % value)

def get_gpj_index(price, eval_price):
    '''
>>> get_gpj_index(11, 100.0)
5.0
>>> get_gpj_index(11, 10.0)
8.0
>>> get_gpj_index(9, 10.0)
8.0
>>> get_gpj_index(9, 9.1)
9.8
>>> get_gpj_index(3.4827, 4)
7.4
    '''
    eval_price = float(eval_price)
    delta = abs(float(price) - eval_price) / eval_price
    return decimal(5 if delta > 0.25 else (10 - 20*delta))
