#!/usr/bin/env python
#-*-coding:utf-8-*-
""" 273.cn 处理器 """
import re
from gpjspider.utils.constants import *

def dmodel(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        d1, d2 = value
        if re.search(u'\d+款', d2):
            year = re.search(u'\d+款', d2).group()

            return year.strip() + ' ' + d1.strip()
        return d1
    return value
