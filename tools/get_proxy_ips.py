# -*- coding: utf-8 -*-
"""
提取从daili666.com购买的代理 IP
"""
import requests


def get_proxy_ips():
    ips = []
    # 淘宝订单号
    tid = "556975388268192"
    # filter=on 过滤提取过的，  num 提取的数量
    api = "http://erwx.daili666.com/ip/?tid={0}&filter=on&num=5000".format(tid)
    try:
        response = requests.get(api)
    except:
        return []
    if response.status_code == 200:
        ips = response.content.split("\r\n")
    if ips:
        f = open('/home/gpjspider/projects/gpjspider/ips.txt', 'a+')
        for ip in ips:
            f.write(ip+'\n')
    return ips

if __name__ == '__main__':
    get_proxy_ips()
