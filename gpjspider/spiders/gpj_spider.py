#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.spiders.base_spiders.incrspider import IncrSpider
import os


class GPJSpider(IncrSpider):
    name = 'gpj_spider'

    def __init__(self, site, type='incr', *args, **kwargs):
        rule_name = '%s.%s' % (type, site)
        self.name = '%s.%s' % (rule_name, os.getpid())
        if type == 'full':
            cls = GPJBaseSpider
        elif type == 'incr':
            cls = IncrSpider
            rule_name = site
        cls.__init__(self, rule_name)
