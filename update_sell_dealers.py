#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gpjspider.tasks.clean.usedcars import update_sell_dealers
import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--step", default=500, help="每一步更新多少")
    parser.add_argument("-l", "--limit", default=0, help="是否只采样更新部分")
    parser.add_argument("-a", "--async", default=0, help="async update")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    update_sell_dealers(int(args.step), int(args.limit), args.async)
