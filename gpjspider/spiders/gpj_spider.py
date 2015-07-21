# -*- coding: utf-8 -*-
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.spiders.base_spiders.incrspider import IncrSpider
import os
import re

__all__ = [
    'IncrGPJSpider',
    'FullGPJSpider',
]


class GPJSpider(IncrSpider):
    type_ = None

    def __init__(self, *args, **kwargs):
        site = self.name.split('_')[0]
        type_ = self.type_
        rule_name = '%s.%s' % (type_, site)
        self.name = '%s.%s' % (rule_name, os.getpid())
        cls = None
        if type_ == 'full':
            cls = GPJBaseSpider
        elif type_ == 'incr':
            cls = IncrSpider
            rule_name = site

        if cls:
            cls.__init__(self, rule_name)


class IncrGPJSpider(GPJSpider):
    type_ = 'incr'


class FullGPJSpider(GPJSpider):
    type_ = 'full'
    _incr_enabled = False


def create_spiders():
    here = os.path.dirname(__file__)
    file_list = os.listdir('%s/rules/full' % os.path.dirname(here))
    rules = re.findall('([a-z\d]+)\.py[^c\.]', ' '.join(file_list))
    for name in 'sample utils test'.split():
        if name in rules:
            rules.remove(name)

    spiders = '# -*- coding: utf-8 -*-\nfrom gpj_spider import *\n'
    spider_cls = """
class Incr{0}GPJSpider(IncrGPJSpider):
    name = '{0}'

class Full{0}GPJSpider(FullGPJSpider):
    name = '{0}_full'
"""
    for rule_name in rules:
        spiders += spider_cls.format(rule_name)

    with open(os.path.join(here, 'auto_spiders.py'), 'w') as fp:
        fp.write(spiders)
        exec spiders

try:
    from auto_spiders import *
except ImportError as e:
    print 'Generating auto spiders..'
    create_spiders()
