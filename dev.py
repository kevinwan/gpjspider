#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import ipdb
from gpjspider.tasks.spiders import *
from gpjspider.tasks.clean.usedcars import clean_domain, clean_item, match_item_dealer, update_eval_price_and_gpj_index
import argparse
import logging


def parse_args():
    """ 解析从命令行读取参数 """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", default="58", help="要执行的网站名称，默认为 58")
    parser.add_argument(
        "-d", "--debug", default=True, help="是否debug模式运行，True/False，默认是 True")
    parser.add_argument(
        "-t", "--dtype", default="incr", help="网站抓取模式，incr/full，默认incr")
    parser.add_argument(
        "-l", "--logger", default="", help="bug追踪日志保存方式，sentry/db，默认sentry")
    parser.add_argument(
        "-u", "--update", default=False, help="是否更新，False/True，默认False")
    parser.add_argument(
        "-p", "--update_price", default=False, help="是否只更新价格指数，False/True，默认False")
    args = parser.parse_args()
    return args


def main(name='test', type_='incr', update=False):
    # import ipdb;ipdb.set_trace()
    sid = None
    act = None
    try:
        act,sid = re.search(r'^(\.|%)([a-zA-Z0-9,\.-]+)$', name).groups()
    except:
        pass

    if act and sid:
        if sid.isdigit() or ',' in sid:
            if act=='.':
                method = clean_item
            elif act=='%':
                method = match_item_dealer
            return [method(int(_sid)) for _sid in sid.split(',')]
        else:
            return clean_domain(sid)
    print '*' * 80

    if name == '.':
        return clean_domain()
    elif name == '?':
        test = GPJSpider('ganji')
    else:
        try:
            eval('run_%s_spider' % type_)(name, update)
        except:
            run_spider('%s.%s' % (type_, name), update)


def setup_logging(log_filename=''):
    import logging
    import datetime

    if not log_filename:
        log_filename = '/tmp/gpjspider/clean_%s.log' % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logging.getLogger('requests').handlers=[]
    return
    logger = logging.getLogger('clean')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

if __name__ == '__main__':
    args = parse_args()
    name = args.site
    type_ = args.dtype
    update = args.update
    update_price = args.update_price
    # ipdb.set_trace()
    if update_price:
        update_eval_price_and_gpj_index(name)
    else:
        if name == '.' or name.startswith('.'):
            setup_logging(args.logger)
        main(name, type_, update)
    # 服务器状态不是很稳定，展示不要把所有log发过去，处理不过来
    # if args.logger=='sentry':
    #     from gpjspider.utils.tracker import hook_logger
    #     hook_logger()
