# -*- coding: utf-8 -*-
from ..full.taoche import rule as old
from . import make_incr_rule

start_urls = [
    'http://www.taoche.com/all/?page=2',
    'http://www.taoche.com/all/?page=3',
    'http://www.taoche.com/all/?page=4',
    'http://www.taoche.com/all/?page=5',
    'http://www.taoche.com/all/?page=6',
]

rule = make_incr_rule(old, start_urls)
