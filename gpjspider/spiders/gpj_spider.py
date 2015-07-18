#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.spiders.base_spiders.incrspider import IncrSpider
import os


class GPJSpider(IncrSpider):
    name = 'gpj_spider'
    site = 'test'
    site = 'baixing'
    type_ = 'incr'

    def __init__(self, site='', type_=None, *args, **kwargs):
        site = site or self.site
        type_ = type_ or self.type_
        rule_name = '%s.%s' % (type_, site)
        self.name = '%s.%s' % (rule_name, os.getpid())
        if type_ == 'full':
            cls = GPJBaseSpider
        elif type_ == 'incr':
            cls = IncrSpider
            rule_name = site
        cls.__init__(self, rule_name)


class IncrGPJSpider(GPJSpider):
    name = 'gpj_incr_spider'


class FullGPJSpider(GPJSpider):
    name = 'gpj_full_spider'
    type_ = 'full'


class GanjiIncrGPJSpider(IncrGPJSpider):
    name = 'ganji_incr_spider'
    site = 'ganji'
    eval('name = %s_incr_spider' % site)(name)
