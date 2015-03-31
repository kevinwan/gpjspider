# -*- coding: utf-8 -*-
"""
规则检查
"""
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME
from gpjspider.checkers import DefaultRuleChecker


class RuleChecker(DefaultRuleChecker):
    """
    """
    name = HIGH_QUALITY_RULE_CHECKER_NAME

    def check(self):
        """
        实现具体的检车规则
        """
        return self.rule
