# -*- coding: utf-8 -*-
u"""
增量爬取爬虫
"""
from .gpjbasespider import GPJBaseSpider
from gpjspider.utils.path import import_incr_rule
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME
from gpjspider.rules.incr import make_incr_rule

class IncrSpider(GPJBaseSpider):
    name = "incrspider"
    _incr_enabled = True

    def __init__(self, rule_name="", update=None, dealer=False, checker_name=HIGH_QUALITY_RULE_CHECKER_NAME):
        if import_incr_rule(rule_name):
            rule_name = 'incr.' + rule_name
        else:
            rule_name = 'full.' + rule_name

        super(IncrSpider, self).__init__(rule_name, update, dealer)

    def setup_rule(self, rule_name):
        # if rule_name.startswith('full'):
        self.website_rule = make_incr_rule(self.website_rule)
