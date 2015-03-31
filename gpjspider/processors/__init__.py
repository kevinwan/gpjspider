# -*- coding: utf-8 -*-
"""
自定义 processor
在字段规则定义中，processor路径是基于 gpjspider.processors的，
如 cheyipai.year 表示 cheyipai 模块的 year函数

processor暂不支持除 value 之外的参数
"""

# common 是基本 processor，在规则配置中直接使用其名称即可
from .common import *
