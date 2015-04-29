# -*- coding: utf-8 -*-
from ..full.che168 import rule as old
from . import make_incr_rule

start_urls = [
    'http://www.che168.com/china/a0_0msdgscncgpiltocsp2ex/',
    'http://www.che168.com/china/a0_0msdgscncgpiltocsp3ex/',
    'http://www.che168.com/china/a0_0msdgscncgpiltocsp4ex/',
]

rule = make_incr_rule(old, start_urls)
