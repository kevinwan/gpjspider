# -*- coding: utf-8 -*-
import os
import sys
import ipdb
import time
import random
import datetime
import requests
import argparse
sys.path.append("..")
from sqlalchemy import func
from threading import Thread, Lock
from scrapy.selector import Selector
from gpjspider.models import UsedCar, CarSource, CarDetailInfo
from gpjspider.utils import get_mysql_connect, get_redis_cluster
from gpjspider.tasks.spiders import run_all_spider_update
from gpjspider.scrapy_settings import PROXIES, PROXY_USER_PASSWD


# 判断是否下线的规则,后期预计简化
domain_dict = {
    '273.cn': [
        [
            u'boolean(//div[@class="tips_shelf"]/strong[contains(text(),"非常抱歉，该车辆已下架")])',
            u'boolean(//div[@id="page404"]/div[@class="tishi" and contains(text(), "后页面自动跳转")])'
        ],
        '1', '273'
    ],    # 404
    '2sc.sohu.com': [
        [
            'boolean(//div[@class="sellico"])'
        ],
        '1', 'sohu'
    ],    # 302
    '51auto.com': [
        [
            'boolean(//div[@class="tishimain"]/span[2]/text())'
        ],
        '1', '51auto'
    ],
    '58.com': [
        [
            'boolean(//div[@class="content clearfix"])',
            u'boolean(//p[@class="lineheight_2"]/span[contains(text(), "信息已过期")]/text())'
        ],
        '1', '58'
    ],
    '99haoche.com': [
        [
            'boolean(//div[@class="sold-out clearfix"])',
            u'boolean(//a[contains(text(),"很抱歉，您访问的车辆已下架，看看其他汽车吧")])'
        ],
        '1', '99haoche'
    ],
    'baixing.com': [
        [
            'boolean(//h3[@class="alert-header"])'
        ],
        '1', 'baixing'
    ],
    'c.cheyipai.com': [
        [
            'boolean(//div[@class="bcz"])',
            'boolean(//div[@class="error"])'
        ],
        '1', 'cheyipai'
    ],    # 404
    'carking001.com': [
        [
            'boolean(//div[@class="se_1"])',
            'boolean(//b[@class="type_1"])',
            'boolean(//b[@class="type_2"])',
            'boolean(//div[@class="info info_1"])'
        ],
        '1', 'carking001'
    ],
    'che168.com': [
        [
            u'boolean(//div[@class="wrong_page"]/p[contains(text(),"访问的车辆信息已失效")])',
            'boolean(//div[@class="plaint-list"])',
            'boolean(//input[@id="hf_CarStatue"]/@value=15)'
        ],
        '1', 'che168'],    # 302
    'chemao.com.cn': [
        [
            'boolean(//div[@class="events_mark04"]/img)',
            'boolean(//div[@class="car-status"]/img)'
        ],
        '1', 'chemao'
    ],    # 500
    'cheshi.com': [
        [
            'boolean(//meta[@content="0;url=http://2sc.cheshi.com/404.shtml"])',
            u'boolean(//div[@class="sc-recommand clearfix mt sc_msg2"]/h4[contains(text(),"暂无此二手车相关信息内容")])'
        ],
        '1', 'cheshi'],    # 404
    'cn2che.com': [
        [
            '//div[@id="carselled"]/@style'
        ],
        'display:;', 'cn2che'
    ],    # 404
    'ganji.com': [
        [
            u'boolean(//div[@class="error"]/p[contains(text(),"页面没有找到或已删除")])',
            'boolean(//span[@class="telephone"]/img[contains(@src,"http://sta.ganjistatic1.com/src/image/v5/expire.png")])'
        ],
        '1', 'ganji'
    ],    # 404
    'haoche.ganji.com': [
        [
            'boolean(//a[@class="stipul-btn stipul-btn-gray"])',
            'boolean(//p[@class="error-tips1"])'
        ],
        '1', 'ganjihaoche'
    ],
    'haoche51.com': [
        [
            u'boolean(//div[@class="cnt-404"]//div[contains(text(),"页面不存在")])',
            'boolean(//div[@class="car-has-deal"])'
        ],
        '1', 'haoche51'
    ],    # 404
    'hx2car.com': [
        [
            'boolean(//*[@class="error_zmb"])',
            u'boolean(//*[contains(text(),"车辆已过期")])'
        ],
        '1', 'hx2car'
    ],
    'iautos.cn': [
        [
            'boolean(//*[contains(@class,"cd-call-sold")])',
            'boolean(//*[contains(@class,"cd-call-exceed")])',
            u'boolean(//p[@class="gy" and contains(text(), "该车已过有效期")])'
        ],
        '1', 'iautos'
    ],    # 404
    'jcjp.com.cn': [
        [
            u'boolean(//span[@class="carprice24redb" and contains(text(), "已经订购")])',
            u'boolean(//*[contains(text(),"暂无车辆信息")])'
        ],
        '1', 'jcjp'
    ],
    'renrenche.com': [
        [
            'boolean(//button[@id="sold_button"])',
            u'boolean(//div[@class="container error"]//*[contains(text(),"这个页面开车离开网站了")])'
        ],
        '1', 'renrenche'
    ],
    'souche.com': [
        [
            'boolean(//div[@id="pageError"])',
            'boolean(//ins[@class="detail-no"])'
        ],
        '1', 'souche'
    ],
    'taoche.com': [
        [
            'boolean(//p[@class="tc14-cyyis"])',
            u'boolean(//div[@class="box worry"])'
        ],
        '1', 'taoche'
    ],    # 302
    'used.xcar.com.cn': [
        [
            'boolean(//i[@class="expired"])'
        ],
        '1', 'xcar'
    ],    # 301 404
    'xin.com': [
        [
            'boolean(//div[@class="d-photo img-album"]/em)',
            u'boolean(//div[@class="error-wrap"]/div[@class="con"]/span[contains(text(),"页面找不到")])'
        ],
        '1', 'xin'
    ],    # 404
    'ygche.com.cn': [
        [
            'boolean(//a[@class="already-buy"])'
        ],
        '1', 'ygche'
    ],    # 302
    'youche.com': [
        [
            '//body/text()'
        ],
        '\r\nerror\r\n\r\n\r\n', 'youche'
    ],    # 302
    'zg2sc.cn': [
        [
            u'boolean(//div[@class="carfile_xinxi_title"]/p[contains(text(),"已售")])'
        ],
        '1', 'zg2sc'
    ]    # 404
}

firewall_rule = {
    '58.com': [
        '//div[@class="search_tips_input"]',
        'Selector(text=web_page.text).xpath(firewall_rule[domain][0]).extract()'
    ],
    'baixing.com': [
        '/html/body/p[contains(text(),"Service Unavailable For") or contains(text(),"Temporarily disabled. Please reduce your visit frequency.")]',
        'Selector(text=web_page.text).xpath(firewall_rule[domain][0]).extract()'
    ],
    'ganji.com': [
        u'//title[contains(text(),"机器人确认") or contains(text(),"反爬虫页面")]',
        'Selector(text=web_page.content).xpath(firewall_rule[domain][0]).extract()'
    ],
}


Session = get_mysql_connect()
redis_bad_ip = get_redis_cluster()
account = PROXY_USER_PASSWD[0].split(':')
auth = requests.auth.HTTPProxyAuth(account[0], account[1])

rule_names = []    # 记录需要更新的网站
num = 1    # 记录程序运行开始共更新了多少条记录
num_per_hour = 1    # 记录当前一小时段内的记录被更新了多少条
lock = Lock()
thread_num = 20    # 依次并发的线程数
range_url_count = 10    # 同一个链接最多尝试访问的次数
range_item_count = 5    # 同一条记录最多尝试更新的次数
uponline = False
log_name = 'log/update.log'


def get_sales_status(domain, url):    # 判断是否下线,代理问题有待解决
    global range_url_count
    web_page = None
    for error_count in range(0, range_url_count):
        try:
            proxies = {'http': random.choice(PROXIES)}
            web_page = requests.get(url, proxies=proxies, auth=auth, timeout=3)
            if web_page.status_code == 407:    # 代理不可用时用本地ip访问
                web_page = requests.get(url)
            # web_page = requests.get(url)
            if domain in ['58.com', 'baixing.com', 'ganji.com'] and eval(firewall_rule[domain][1]):
                raise Exception(['Website shield and all agent failure !'])
        except Exception as e:
            try:
                error_string = ''.join(e.args)
            except Exception:
                error_string = e.message.message
            finally:
                if web_page:
                    if 'x-proxymesh-ip' in web_page.headers and 'Website shield and all agent failure' in error_string:
                        invalid_ip_key = domain + str(datetime.date.today())
                        redis_bad_ip.sadd(invalid_ip_key, web_page.headers['x-proxymesh-ip'])
                if error_count + 1 == range_url_count:
                    error_string = '\n' + url + ' ' + error_string
                    return ['online', error_string]
        else:
            break
    if web_page:
        if domain == 'zg2sc.cn' and not web_page.content:
            return 'offline'
        if domain in ['jcjp.com.cn', 'zg2sc.cn']:
            response = Selector(text=web_page.content.decode('gb2312', 'replace'))
        else:
            if domain in ['ganji.com', 'haoche51.com', 'renrenche.com', 'xin.com']:
                response = Selector(text=web_page.content)
            else:
                response = Selector(text=web_page.text)
        if 'x-proxymesh-ip' not in web_page.headers:    # 本机ip访问时降低访问速度
            time.sleep(1)
        xpaths = domain_dict[domain][0]
        for xpath in xpaths:
            sales = response.xpath(xpath).extract()
            if sales:
                if sales[0] == domain_dict[domain][1]:
                    return 'offline'
    return 'online'


def get_update_time(item, time_now):    # 计算下次更新时间,待优化
    time_def = None
    next_update_time = (
        datetime.datetime.now() + datetime.timedelta(
            days=1,
            seconds=0
        )
    )
    if item.next_update > item.last_update:
        time_def = item.next_update - item.last_update
    else:
        time_def = item.last_update - item.next_update
    if time_def.days + time_def.seconds > 0:
        time_def.days = 1    # 目前默认更新间隔为1天，这里将不是1天的强制设为1天，后期有待改进
        time_def.seconds = 0
        next_update_time = (
            time_now + datetime.timedelta(
                days=time_def.days,
                seconds=time_def.seconds
            )
        )
    return next_update_time


# 更新原始表和业务表的车源的销售状态
def update_sale_status(site=None, days=None, before=None):
    session = Session()
    global rule_names
    global log_name
    if not os.path.isdir('log'):
        os.mkdir('log')
    log_name = 'log/update'    # 日志文件名
    if uponline:
        log_name = log_name + '_uponline'
    if site:
        log_name = log_name + '_' + site
    # 计算需要更新的车源对应的创建时间,按每1小时分块依次递减查询数据
    time_now = datetime.datetime.now()
    if not days:
        after_time = session.query(func.min(UsedCar.created_on)).scalar()
    else:
        after_time = time_now - datetime.timedelta(days=days - 1)
    after_time = after_time.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
    if before:
        day_on = datetime.datetime.strptime(before, '%Y-%m-%d %H:%M:%S').replace(
            minute=0,
            second=0,
            microsecond=0
        ) + datetime.timedelta(seconds=3600)
    else:
        day_on = time_now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        ) + datetime.timedelta(days=1)
    log_name = log_name + '_[' + time_now.strftime("%Y-%m-%d %H:%M:%S") + ']'
    log_name = log_name + ' [' + after_time.strftime("%Y-%m-%d %H:%M:%S") + ']-'
    log_name = log_name + '[' + day_on.strftime("%Y-%m-%d %H:%M:%S") + ']'
    log_name = log_name + '.log'
    file_object = open(log_name, 'w')    # 如果文件存在就清空内容
    file_object.write('')
    file_object.close()
    day_up = day_on - datetime.timedelta(seconds=3600)
    session.close()

    while day_up >= after_time:
        # 查询1小时需要更新的车源
        session = Session()
        query = session.query(
            UsedCar.domain,
            UsedCar.url,
            UsedCar.status,
            UsedCar.update_count,
            UsedCar.id,
            UsedCar.created_on,
            UsedCar.next_update,
            UsedCar.last_update
        )
        if site:
            site_dict = {value[2]: key for key, value in domain_dict.items()}
            domain = site_dict[site]
            query = query.filter(UsedCar.domain == domain)
        query = query.filter(
            UsedCar.status == 'C',
            UsedCar.created_on != None,
            UsedCar.created_on >= day_up,
            UsedCar.created_on < day_on,
            UsedCar.next_update != None,
            UsedCar.last_update != None,
            UsedCar.next_update <= time_now
        )
        num_this_hour = query.count()
        # if num_this_hour > 0:
        log_str = ' '.join([
            '\n\n' + '[' + str(after_time) + ']',
            '[' + str(day_up) + ']-[' + str(day_on) + ']',
            str(num_this_hour)
        ])
        file_object = open(log_name, 'a')
        file_object.write(log_str)
        file_object.close()
        day_up = day_up - datetime.timedelta(seconds=3600)
        day_on = day_on - datetime.timedelta(seconds=3600)
        items = query.all()
        session.close()
        deal_items(items)
    if rule_names:
        run_all_spider_update(rule_names)    # 更新所有未下线的车源


def deal_items(items):    # 单独提出模块，方便调用
    global thread_num
    global num_per_hour
    num_per_hour = 1
    num_this_hour = len(items)
    thread_list = []
    for item in items:
        child_thread = Thread(
            target=deal_one_item,
            args=(item, num_this_hour)
        )
        thread_list.append(child_thread)
        if len(thread_list) == thread_num:
            for child_thread in thread_list:
                child_thread.start()
            for child_thread in thread_list:
                child_thread.join()
            thread_list = []
    for child_thread in thread_list:
        child_thread.start()
    for child_thread in thread_list:
        child_thread.join()


def deal_one_item(item, num_this_hour):
    global num
    global lock
    global log_name
    global uponline
    global rule_names
    global num_per_hour
    global range_item_count

    for error_count in range(0, range_item_count):
        error_string = None
        new_error_string = None
        session = None
        sales_status = 'online'    # 设置默认值
        time_now = datetime.datetime.now()    # 设置默认值
        try:
            session = Session()
            sales_status = get_sales_status(item.domain, item.url)
            time_now = datetime.datetime.now()
            if isinstance(sales_status, list):
                error_string = sales_status[1]
                sales_status = sales_status[0]
            if sales_status == 'offline':
                status = 'Q'    # 已下线的变为'Q'
                # 同步更新car_source状态
                session.query(CarSource).filter(
                    CarSource.url == item.url
                ).update(
                    {CarSource.status: 'review'},
                    synchronize_session=False
                )
                # 同步更新car_detail_info的update_time字段
                session.query(CarDetailInfo).filter(
                    CarSource.url == item.url,
                    CarDetailInfo.car_id == CarSource.id
                ).update(
                    {
                        CarDetailInfo.update_time: time_now,
                        CarDetailInfo.car_id: CarSource.id
                    },
                    synchronize_session=False
                )
            else:
                if uponline:
                    status = 'u'  # 未下线的变为'u'
                    rule_name = domain_dict[item.domain][2]
                    if rule_name not in rule_names:
                        rule_names.append(rule_name)
                else:
                    status = item.status
            # 更新单条记录
            if not item.update_count:
                update_count = 0
            else:
                update_count = item.update_count
            session.query(UsedCar).filter(UsedCar.url == item.url).update(
                {
                    UsedCar.status: status,
                    UsedCar.last_update: time_now,
                    UsedCar.next_update: get_update_time(item, time_now),
                    UsedCar.update_count: update_count + 1
                },
                synchronize_session=False
            )
        except Exception as e:
            if session:
                session.rollback()
                session.close()
            if error_count + 1 == range_item_count:
                new_error_string = '\n' + item.url + ' deal failure: ' + ''.join(e.args)
        else:
            if session:
                session.commit()
                session.close()
            break
    lock.acquire()    # 加锁，防止变量值错乱
    log_str = ' '.join([
        '\n' + '[' + time_now.strftime("%Y-%m-%d %H:%M:%S") + ']',
        '[' + item.created_on.strftime("%Y-%m-%d %H:%M:%S") + ']',
        str(item.id),
        str(num),
        str(num_per_hour) + '/' + str(num_this_hour),
        sales_status,
        item.url
    ])
    file_object = open(log_name, 'a')
    if error_string:
        file_object.write(error_string)
    if new_error_string:
        file_object.write(new_error_string)
    file_object.write(log_str)
    file_object.close()
    num_per_hour = num_per_hour + 1
    num = num + 1
    lock.release()


# 更新已发现错误的车源
def update_error_status(status=None, site=None, days=7, seconds=0):
    session = Session()
    # 查询错误车源
    query = session.query(UsedCar.domain).filter(
        UsedCar.created_on > (
            datetime.datetime.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ) - datetime.timedelta(
                days=days,
                seconds=seconds
            )
        )
    )
    if site:
        site_dict = {value[2]: key for key, value in domain_dict.items()}
        domain = site_dict[site]
        query = query.filter(UsedCar.domain == domain)
    if status:
        query = query.filter(UsedCar.status == status)
    else:
        query = query.filter(func.length(UsedCar.status) > 2)
    rule_names = []
    for item in query.group_by(UsedCar.domain).all():
        rule_names.append(domain_dict[item.domain][2])
    if rule_names:
        # 标记错误车源
        query.update({UsedCar.status: 'u'}, synchronize_session=False)
        session.commit()
        session.close()
        # 更新错误车源
        run_all_spider_update(rule_names)


def parse_args():
    """ 解析从命令行读取参数 """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--uponline", default=False, help="是否重新爬取未下线的车源,默认为False")
    parser.add_argument("-t", "--status", default=None, help="要更新的错误状态,如-model_slug,默认为None,默认时更新所有错误状态")
    parser.add_argument("-s", "--site", default=None, help="要更新的网站,默认为None,默认时更新所有网站")
    parser.add_argument("-d", "--days", default=None, help="要更新几天以内的记录,默认为最早的那天")
    parser.add_argument("-b", "--before", default=None, help="要更新多久以前的记录,默认为当前时间")
    parser.add_argument("-e", "--seconds", default=None, help="要更新几秒以内的记录,默认为0秒")
    parser.add_argument("-u", "--model", default="offline", help="更新模式,offline为更新下线记录,error为更新错误记录,默认为更新错误记录")
    args = parser.parse_args()
    return args


# 默认更新7天以内的所有错误记录
if __name__ == '__main__':
    args = parse_args()
    uponline = args.uponline
    model = args.model
    status = args.status
    site = args.site
    days = args.days
    before = args.before
    seconds = args.seconds
    if model == 'error':
        try:
            if days:
                days = int(days)
            else:
                days = 7
            if seconds:
                seconds = int(seconds)
            else:
                seconds = 0
        except Exception as e:
            print(e)
        else:
            update_error_status(status, site, days, seconds)
    elif model == 'offline':
        try:
            if days:
                days = int(days)
        except Exception as e:
            print(e)
        else:
            update_sale_status(site, days, before)
    else:
        print 'Input update model is invalid !'
