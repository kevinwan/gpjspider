#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gpjspider.tasks.spiders import *
from gpjspider.tasks.clean.usedcars import clean_domain
import argparse

def parse_args():
    """ 解析从命令行读取参数 """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", default="58", help="要执行的网站名称，默认为 58")
    parser.add_argument("-d", "--debug", default=True, help="是否debug模式运行，True/False，默认是 True")
    parser.add_argument("-t", "--dtype", default="incr", help="网站抓取模式，incr/full，默认incr")

    args = parser.parse_args()
    return args

def main(name='test', type_='incr'):
    if name == '.':
        return clean_domain()
    # elif name.endswith('.com'):
    #     clean_domain(name)
    else:
        try:
            eval('run_%s_spider' % type_)(name)
        except:
            run_spider('%s.%s' % (type_, name))

if __name__ == '__main__':
    import sys
    #main(*sys.argv[1:3])
    args = parse_args()
    name = args.site
    type_ = args.dtype

    main(name, type_)
