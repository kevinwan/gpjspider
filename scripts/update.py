# -*- coding: utf-8 -*-
import os
import re
import sys
import ipdb
import time
import random
import datetime
import requests
import argparse
sys.path.append("..")
import StringIO
from PIL import Image
from sqlalchemy import func
from threading import Thread, Lock
from scrapy.selector import Selector
from pytesseract import image_to_string
from gpjspider.models import UsedCar, CarSource, CarDetailInfo
from gpjspider.utils import get_mysql_connect, get_redis_cluster
from gpjspider.tasks.spiders import run_all_spider_update
from gpjspider.scrapy_settings import PROXIES, PROXY_USER_PASSWD
from gpjspider.downloaders.proxymiddleware import get_internal_ip


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
            'boolean(//div[@class="sold-out"])',
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
        '1', 'guazi'
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
            u'boolean(//p[@class="gy" and contains(text(), "该车已过有效期")])',
            u'boolean(//*[contains(@class,"hint clearfix")]//*[contains(text(), "您查看的车源正在审核中或已删除")])',
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
day_up = None
# num_per_hour = 1    # 记录当前一小时段内的记录被更新了多少条
lock = Lock()
thread_num = 20    # 依次并发的线程数
range_url_count = 10    # 同一个链接最多尝试访问的次数
range_item_count = 5    # 同一条记录最多尝试更新的次数
uponline = False
log_name = 'log/update.log'
server_id = '127.0.0.1'
try:
    server_id = get_internal_ip
except Exception as e:
    print u'ExceptionInfo: {0}'.format(e)


def parse_58_firewall(web_page):
    response = Selector(text=web_page.text)
    uuid_list = response.xpath('//input[@id="uuid"]/@value').extract()
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'id58=05dzXFW3KVypm2tvK5JCAg==; __ag_cm_=1438067041103; sessionid=2a4c9cab-78f5-444c-9dca-7fa65288e83f; ag_fid=TvlD8uQkNDpJfwGF; _ga=GA1.2.382082989.1438067359; als=0; xxzl_cp=64248043b2de4dbba0bc7957f5f27165190; vip=v%3D1%26vipuserpline%3D1005%26masteruserid%3D33124437196550%26vipkey%3Da6447f5abbcb274ca0816f851a68c93b%26vipusertype%3D11; myfeet_tooltip=end; bangbigtip2=1; bangtoptipclose=1; 58home=bj; __autmz=253535702.1441729168.1.1.autmcsr=(direct)|autmccn=(direct)|autmcmd=(none); __autma=253535702.157438233.1441729168.1441729168.1441732451.2; __autmc=253535702; __utma=253535702.382082989.1438067359.1441732451.1441951771.19; __utmc=253535702; __utmz=253535702.1441951771.19.7.utmcsr=dl.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/ershouche/23289743015332x.shtml; city=jixi; ipcity=cd%7C%u6210%u90FD; Nprd=26|1442631080529; _vz=viz_55ee973682873; bangbangid=1080863913022601748; new_uv=62; final_history=22668443783049%2C22668435425822%2C22668441197474%2C22668432867492%2C22668651581193; Nvis=48|1442285480528',
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    if uuid_list:
        uuid = uuid_list[0]
        url = 'http://support.58.com/firewall/code/2101784591/6444e593.do?rnd=1'
        while response.xpath('//div[@class="search_tips_input"]').extract():
            equa = None
            while equa is None:
                im = requests.get(url).content
                imob = Image.open(StringIO.StringIO(im))
                imob = imob.convert('RGB')
                text = image_to_string(imob)
                equa = re.search(r'(\d+[\+-]\d+)[:=‘]', text)
            num = str(eval(equa.group(1)))
            bb = requests.post('http://support.58.com/firewall/code/2101784591/6444e593.do', headers = headers, data={'inputcode': num, 'uuid': uuid, 'namespace': u'infodetailweb'})
            print num, bb.text
            web_page = requests.get(web_page.url.split('&url=')[1])
            response = Selector(text=web_page.text)
    return web_page


def get_sales_status(domain, url):    # 判断是否下线,代理问题有待解决
    global range_url_count
    global server_id
    web_page = None
    for error_count in range(0, range_url_count):
        try:
            if domain in ['58.com', 'baixing.com', 'ganji.com']:
                proxies = {'http': random.choice(PROXIES)}
                web_page = requests.get(url, proxies=proxies, auth=auth, timeout=3)
                if web_page.status_code == 407:    # 代理不可用时用本地ip访问
                    web_page = requests.get(url)
                if eval(firewall_rule[domain][1]):
                    raise Exception('Website shield and all agent failure !')
            else:
                web_page = requests.get(url)
            # web_page = requests.get(url)
        except Exception as e:
            try:
                error_string = ''.join(e.args)
            except Exception:
                error_string = e.message.message
            finally:
                if web_page is not None:
                    if 'x-proxymesh-ip' in web_page.headers and 'Website shield and all agent failure' in error_string:
                        key = '%s_%s_%s' % (domain, web_page.status_code, str(datetime.date.today()))
                        redis_bad_ip.sadd(key, url)
                        proxymesh_ip = web_page.headers.get('x-proxymesh-ip')
                        invalid_ip_key = '%s_%s_%s' % (server_id, domain, str(datetime.date.today()))
                        redis_bad_ip.sadd(invalid_ip_key, proxymesh_ip)
                        redis_bad_ip.expire(invalid_ip_key, 600)
                        time.sleep(30)
                        # web_page = parse_58_firewall(web_page)
                if error_count + 1 == range_url_count:
                    error_string = '\n' + url + ' ' + error_string
                    return ['online', error_string]
        else:
            break
    if web_page is not None:
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
    # time_def = None
    # next_update_time = (
    #     time_now + datetime.timedelta(
    #         days=1,
    #         seconds=0
    #     )
    # )
    # if item.next_update > item.last_update:
    #     time_def = item.next_update - item.last_update
    # else:
    #     time_def = item.last_update - item.next_update
    # if time_def.days + time_def.seconds > 0:
    #     next_update_time = (
    #         time_now + datetime.timedelta(
    #             days=time_def.days,
    #             seconds=time_def.seconds
    #         )
    #     )
    next_update_time = (
        time_now + datetime.timedelta(
            days=1
        )
    )
    return next_update_time


# 更新原始表和业务表的车源的销售状态
def update_sale_status(site=None, days=None, before=None, count=0, hours=12):
    session = Session()
    global rule_names
    global log_name
    global day_up
    delta = dict(hours=hours / 2)
    # delta = dict(days=1)
    # delta = dict(hours=1)
    log_dir = '/tmp/gpjspider/'
    # if not os.path.isdir(log_dir):
    #     os.mkdir(log_dir)
    log_name = os.path.join(log_dir, 'update')    # 日志文件名
    if uponline:
        log_name += '_uponline'
    if site:
        log_name += '_' + site
    # 计算需要更新的车源对应的创建时间,按每1小时分块依次递减查询数据
    time_now = datetime.datetime.now()
    if not days:
        start_time = session.query(func.min(UsedCar.created_on)).scalar()
    else:
        start_time = time_now - datetime.timedelta(days=days - 1)
    start_time = start_time.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
    if before:
        end_time = datetime.datetime.strptime(before, '%Y-%m-%d %H:%M:%S').replace(
            minute=0,
            second=0,
            microsecond=0
        ) + datetime.timedelta(**delta)
    else:
        end_time = time_now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        ) - datetime.timedelta(days=1)

    log_name += '_' + time_now.strftime("%Y-%m-%d") + ' '
    log_name += start_time.strftime("%Y.%m.%d") + '-'
    log_name += end_time.strftime("%Y.%m.%d") + '.log'
    # file_object = open(log_name, 'w')    # 如果文件存在就清空内容
    # file_object.write('')
    # file_object.close()
    # day_on = end_time
    # day_up = day_on - datetime.timedelta(**delta)
    day_up = start_time
    day_on = day_up + datetime.timedelta(**delta)
    session.close()

    # while day_up >= start_time:
    while day_on <= end_time:
        # 查询4小时需要更新的车源
        session = Session()
        query = session.query(
            UsedCar.id,
            UsedCar.url,
            UsedCar.domain,
            UsedCar.update_count,
        )
        if site:
            site_dict = {value[2]: key for key, value in domain_dict.items()}
            domain = site_dict[site]
            query = query.filter(UsedCar.domain == domain)
        query = query.filter(
            # UsedCar.created_on is not None,
            UsedCar.created_on >= day_up,
            UsedCar.created_on < day_on,
            # UsedCar.status.in_(['C', 'Y']),
            UsedCar.status == 'C',
            UsedCar.update_count <= count,
            UsedCar.next_update <= time_now,
            # UsedCar.next_update is not None,
            # UsedCar.last_update is not None,
        )
        lmt = 60
        # lmt = 100
        psize = 5
        items = query.limit(lmt).yield_per(psize)
        size = items.count()
        if not size:
            print day_on, size
        while size:
            print day_on, size
            deal_items(items)
            items = query.limit(lmt).yield_per(psize)
            size = items.count()
        session.close()
        # day_up -= datetime.timedelta(**delta)
        # day_on -= datetime.timedelta(**delta)
        day_up += datetime.timedelta(**delta)
        day_on += datetime.timedelta(**delta)
    if rule_names:
        run_all_spider_update(rule_names)    # 更新所有未下线的车源


def deal_items(items):    # 单独提出模块，方便调用
    global thread_num
    # global num_per_hour
    # num_per_hour = 1
    # num_this_hour = len(items)
    thread_list = []
    for item in items:
        child_thread = Thread(
            target=deal_one_item,
            # args=(item, num_this_hour),
            args=(item, ),
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


def deal_one_item(item, num_this_hour=None):
    global num
    global lock
    global day_up
    global log_name
    global uponline
    global rule_names
    # global num_per_hour
    global range_item_count

    for error_count in range(0, range_item_count):
        error_string = None
        new_error_string = None
        session = None
        update_dict = {}
        sales_status = 'online'    # 设置默认值
        time_now = datetime.datetime.now()    # 设置默认值
        try:
            session = Session()
            sales_status = get_sales_status(item.domain, item.url)
            if item.domain == '58.com' and sales_status == 'offline':
                # time.sleep(1)
                sales_status = get_sales_status(item.domain, item.url)
            time_now = datetime.datetime.now()
            if isinstance(sales_status, list):
                error_string = sales_status[1]
                sales_status = sales_status[0]
            if sales_status == 'offline':
                update_dict[UsedCar.status] = 'Q'    # 已下线的变为'Q'
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
                    update_dict[UsedCar.status] = 'u'  # 未下线的变为'u'
                    rule_name = domain_dict[item.domain][2]
                    if rule_name not in rule_names:
                        rule_names.append(rule_name)
            # 更新单条记录
            if not item.update_count:
                update_count = 0
            else:
                update_count = item.update_count
            update_dict[UsedCar.last_update] = time_now
            update_dict[UsedCar.next_update] = get_update_time(item, time_now)
            update_dict[UsedCar.update_count] = update_count + 1
            session.query(UsedCar).filter(UsedCar.url == item.url).update(
                update_dict,
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
        str(item.id) + '@' + day_up.strftime("%Y-%m-%d"),
        str(num),
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
    # num_per_hour = num_per_hour + 1
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
    parser.add_argument("-d", "--days", default=None, help="要更新包括今天在内的共几天的记录,默认为最早的那天")
    parser.add_argument("-hs", "--hours", default=None)
    parser.add_argument("-c", "--count", default=None)
    parser.add_argument("-b", "--before", default=None, help="要更新多久以前的记录,默认为当前时间")
    # parser.add_argument("-e", "--seconds", default=None, help="要更新几秒以内的记录,默认为0秒")
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
    count = args.count
    hours = args.hours
    before = args.before
    if model == 'error':
        try:
            days = int(days) if days else 7
        except Exception as e:
            print(e)
        else:
            update_error_status(status, site, days)
    elif model == 'offline':
        try:
            # magic = bool(count)
            count = int(count) if count else 0
            hours = int(hours) if hours else 12
            if days:
                days = int(days)
            else:
                days = 60
                # days /= 2**(4 - count)
                days /= (1 + count)
                days += 1
        except Exception as e:
            print(e)
        else:
            update_sale_status(site, days, before, count, hours)
    # else:
    #     print 'Input update model is invalid !'
