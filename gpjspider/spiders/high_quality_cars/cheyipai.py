# -*- coding: utf-8 -*-
"""
车易拍 优质二手车
"""
from prettyprint import pp
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME


class HighQualityCarSpider(GPJBaseSpider):
    """
    """
    name = "high_quality_car"

    def __init__(self, rule_name="cheyipai",
                 checker_name=HIGH_QUALITY_RULE_CHECKER_NAME):
        """
        HQCar  for HighQualityCar
        """
        super(HighQualityCarSpider, self).__init__(rule_name)
        self.__checker_name = checker_name
        self.checker_class = self.checker_manager.get_checker(checker_name)
        self.checker = self.checker_class(rule_name)
        self.website_rule = self.checker.check()
        pp(self.website_rule)
        if not self.website_rule:
            raise ValueError('TODO')
        self.domain = self.website_rule['domain']
