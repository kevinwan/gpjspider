# -*- coding: utf-8 -*-
"""
增量爬取爬虫
"""
import inspect
from prettyprint import pp, pp_str
from rediscluster import RedisCluster
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem
from gpjspider.utils.path import import_rule_function, import_item
from gpjspider.utils.path import import_processor
from gpjspider.checkers import CheckerManager
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME

from .gpjbasespider import GPJBaseSpider


class IncrSpider(GPJBaseSpider):
    """
    """
    name = "incrspider"

    def __init__(self, rule_name="", checker_name=HIGH_QUALITY_RULE_CHECKER_NAME):
        super(IncrSpider, self).__init__(rule_name)
        self.__checker_name = checker_name
        self.checker_class = self.checker_manager.get_checker(checker_name)
        self.checker = self.checker_class(rule_name)
        self.website_rule = self.checker.check()
        pp(self.website_rule)
        if not self.website_rule:
            raise ValueError('TODO')
        self.domain = self.website_rule['domain']

    