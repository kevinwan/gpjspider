# -*- coding: utf-8 -*-
"""
增量爬取爬虫
"""
from prettyprint import pp
from gpjspider.utils.path import import_incr_rule
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME

from .gpjbasespider import GPJBaseSpider


class IncrSpider(GPJBaseSpider):
    """
    """
    name = "incrspider"

    def __init__(self, rule_name="", checker_name=HIGH_QUALITY_RULE_CHECKER_NAME):
        if import_incr_rule(rule_name):
            rule_name = 'incr.' + rule_name
        super(IncrSpider, self).__init__(rule_name)
        self.__checker_name = checker_name
        self.checker_class = self.checker_manager.get_checker(checker_name)
        self.checker = self.checker_class(rule_name)
        self.website_rule = self.checker.check()
        pp(self.website_rule)
        if not self.website_rule:
            raise ValueError('TODO')
        self.domain = self.website_rule['domain']
