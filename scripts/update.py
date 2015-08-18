# -*- coding: utf-8 -*-
import sys
import ipdb
import datetime
import requests
import argparse
sys.path.append("..")
from sqlalchemy import func
from scrapy.selector import Selector
from gpjspider.models import UsedCar, CarSource, CarDetailInfo
from gpjspider.utils import get_mysql_connect
from gpjspider.tasks.spiders import run_all_spider_update

Session = get_mysql_connect()

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
    'cheshi.com': [[], '', 'cheshi'],    # 404    #*******
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

auth = requests.auth.HTTPProxyAuth('gaoge', 'gaoge911911')
proxies = {'http': 'http://us-il.proxymesh.com:31280'}


def get_sales_status(domain, url):    # 判断是否下线,代理问题有待解决
    for error_count in [0, 1, 2, 3, 4]:
        try:
            web_page = requests.get(url, proxies=proxies, auth=auth, timeout=5)
            if web_page.status_code == 407:
                web_page = requests.get(url)
        except Exception as e:
            error_count = error_count + 1
            if error_count == 5:
                file_object = open('update.log', 'a')
                file_object.write('\n' + url + ' ' + ''.join(e.args))
                file_object.close()
                return 'online'
        else:
            break
    if domain == 'zg2sc.cn' and not web_page.content:
        return 'offline'
    if domain in ['jcjp.com.cn', 'zg2sc.cn']:
        response = Selector(text=web_page.content.decode('gb2312', 'replace'))
    else:
        if domain in ['ganji.com', 'haoche51.com', 'renrenche.com', 'xin.com']:
            response = Selector(text=web_page.content)
        else:
            response = Selector(text=web_page.text)
    xpaths = domain_dict[domain][0]
    for xpath in xpaths:
        sales = response.xpath(xpath).extract()
        if sales:
            if sales[0] == domain_dict[domain][1]:
                return 'offline'
    return 'online'


def get_update_time(item):    # 计算下次更新时间,待优化
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
    if time_def.seconds > 0:
        next_update_time = (
            datetime.datetime.now() + datetime.timedelta(
                days=time_def.days * 2,
                seconds=time_def.seconds * 2
            )
        )
    return next_update_time


# 更新原始表和业务表的车源的销售状态
def update_sale_status(uponline=False, site=None, days=None):
    session = Session()
    # 计算需要更新的车源对应的创建时间,按每三小时分块依次递减查询数据
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
    day_on = time_now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    ) + datetime.timedelta(days=1)
    day_up = day_on - datetime.timedelta(seconds=3600)
    num = 1
    session.close()
    while day_up >= after_time:
        # ipdb.set_trace()
        # 查询三小时需要更新的车源
        session = Session()
        query = session.query(
            UsedCar.domain,
            UsedCar.url,
            UsedCar.status,
            UsedCar.update_count,
            UsedCar.id,
            UsedCar.next_update,
            UsedCar.last_update
        )
        if site:
            site_dict = {value[2]: key for key, value in domain_dict.items()}
            domain = site_dict[site]
            query = query.filter(UsedCar.domain == domain)
        query = query.filter(
            UsedCar.created_on != None,
            UsedCar.created_on >= day_up,
            UsedCar.created_on < day_on
        )
        query = query.filter(
            UsedCar.status != 'Q',
            UsedCar.status != 'u',
            UsedCar.status != 'I',
            UsedCar.next_update != None,
            UsedCar.last_update != None,
            UsedCar.update_count == 0,
            UsedCar.next_update <= time_now
        )
        num_per_hour = 1
        num_this_hour = query.count()
        # if num_this_hour > 0:
        log_str = ' '.join([
            '\n\n' + '[' + str(after_time) + ']',
            '[' + str(day_up) + ']-[' + str(day_on) + ']',
            str(num_this_hour)
        ])
        file_object = open('update.log', 'a')
        file_object.write(log_str)
        file_object.close()
        day_up = day_up - datetime.timedelta(seconds=3600)
        day_on = day_on - datetime.timedelta(seconds=3600)
        rule_names = []    # 记录需要更新的网站
        items = query.all()
        session.close()
        for item in items:
            for error_count in [0, 1, 2, 3, 4]:
                try:
                    session = Session()
                    sales_status = get_sales_status(item.domain, item.url)
                    time_now = datetime.datetime.now()
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
                            UsedCar.next_update: get_update_time(item),
                            UsedCar.update_count: update_count + 1
                        },
                        synchronize_session=False
                    )
                    log_str = ' '.join([
                        '\n' + str(num),
                        str(num_per_hour),
                        sales_status,
                        str(item.id),
                        item.url,
                        '[' + time_now.strftime("%Y-%m-%d %H:%M:%S") + ']'
                    ])
                    file_object = open('update.log', 'a')
                    file_object.write(log_str)
                    file_object.close()
                    num_per_hour = num_per_hour + 1
                    num = num + 1
                    session.commit()
                    session.close()
                except Exception as e:
                    session.close()
                    error_count = error_count + 1
                    if error_count == 5:
                        file_object = open('update.log', 'a')
                        file_object.write('\n' + item.url + ' ' + ''.join(e.args))
                        file_object.close()
                else:
                    break
    if rule_names:
        run_all_spider_update(rule_names)    # 更新所有未下线的车源


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
    parser.add_argument("-d", "--days", default=None, help="要更新几天以内的记录,默认为0天")
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
            update_sale_status(uponline, site, days)
    else:
        print 'Input update model is invalid !'
