#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from gpjspider.tasks.spiders import *
from gpjspider.tasks.clean.usedcars import clean_domain, clean_item
import argparse


def parse_args():
    """ 解析从命令行读取参数 """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", default="58", help="要执行的网站名称，默认为 58")
    parser.add_argument(
        "-d", "--debug", default=True, help="是否debug模式运行，True/False，默认是 True")
    parser.add_argument(
        "-t", "--dtype", default="incr", help="网站抓取模式，incr/full，默认incr")
    parser.add_argument(
        "-l", "--logger", default="sentry", help="bug追踪日志保存方式，sentry/db，默认sentry")
    parser.add_argument(
        "-u", "--update", default=False, help="是否更新，False/True，默认False")
    args = parser.parse_args()
    return args


def main(name='test', type_='incr', update=False):
    # import ipdb;ipdb.set_trace()
    sid = None
    try:
        sid = re.search(r'^\.([a-zA-Z0-9\.-]+)$', name).group(1)
    except:
        pass

    if sid:
        if sid.isdigit():
            return clean_item(int(sid))
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

if __name__ == '__main__':
    args = parse_args()
    name = args.site
    type_ = args.dtype
    # 服务器状态不是很稳定，展示不要把所有log发过去，处理不过来
    # if args.logger=='sentry':
    #     from gpjspider.utils.tracker import hook_logger
    #     hook_logger()
    update = args.update
    main(name, type_, update)
