#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.spiders.base_spiders.incrspider import IncrSpider
import os
import re


class GPJSpider(IncrSpider):
    type_ = ''

    def __init__(self, type_=None, *args, **kwargs):
        site = self.name.split('_')[0]
        type_ = type_ or self.type_
        rule_name = '%s.%s' % (type_, site)
        self.name = '%s.%s' % (rule_name, os.getpid())
        if type_ == 'full':
            cls = GPJBaseSpider
        elif type_ == 'incr':
            cls = IncrSpider
            rule_name = site
        else:
            cls = None
        if cls:
            cls.__init__(self, rule_name)


class IncrGPJSpider(GPJSpider):
    type_ = 'incr'


class FullGPJSpider(GPJSpider):
    type_ = 'full'


os.chdir('%s/rules/full' % os.path.dirname(os.path.dirname(__file__)))
file_list = os.listdir(os.getcwd())
rules = re.findall('([\w\d]+)\.py[^c]', ' '.join(file_list))
rules.remove('__init__')
for rule_name in rules:

    exec """class Incr{0}GPJSpider(IncrGPJSpider):
    name = '{0}'

class Full{0}GPJSpider(FullGPJSpider):
    name = '{0}_full'
""".format(rule_name)
