# -*- coding: utf-8 -*-
"""
增量爬取爬虫
"""
from .gpjbasespider import GPJBaseSpider
from prettyprint import pp
from gpjspider.utils.path import import_incr_rule
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME
import copy


def make_incr_rule(full_rule, start_urls=[]):
    rule = copy.deepcopy(full_rule)

    rule['parse']['incr_page_url'] = rule['parse'].pop('next_page_url')
    rule['parse']['incr_page_url'].pop('max_pagenum')
    # rule['parse']['incr_page_url']['max_pagenum'] = 1
    return rule


class IncrSpider(GPJBaseSpider):
    name = "incrspider"

    def __init__(self, rule_name="", checker_name=HIGH_QUALITY_RULE_CHECKER_NAME):
        if import_incr_rule(rule_name):
            rule_name = 'incr.' + rule_name
        else:
            rule_name = 'full.' + rule_name
            # checker_name = 'incr'
        # super(IncrSpider, self).__init__(rule_name, checker_name)
        super(IncrSpider, self).__init__(rule_name)
        # self.__checker_name = checker_name
        # self.checker_class = self.checker_manager.get_checker(checker_name)
        # self.checker = self.checker_class(rule_name)
        # # self.website_rule = make_incr_rule(self.checker.check())
        # self.website_rule = self.checker.check()
        # pp(self.website_rule['parse'])
        # if not self.website_rule:
        #     raise ValueError('TODO')
        # self.domain = self.website_rule['domain']

    def setup_rule(self, rule_name):
        if rule_name.startswith('full'):
            self.website_rule = make_incr_rule(self.website_rule)
