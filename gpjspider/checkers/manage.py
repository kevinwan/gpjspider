# -*- coding: utf-8 -*-
"""
"""

from gpjspider.checkers import DefaultRuleChecker
from gpjspider.checkers.rule import RuleChecker


class CheckerManager:
    """
    """
    def __init__(self):
        self.__checkers = {}
        self.get_all_checkers()

    def get_all_checkers(self):
        self.__checkers = {
            RuleChecker.name: RuleChecker,
            DefaultRuleChecker.name: DefaultRuleChecker
        }
        return self.__checkers

    def get_checker(self, checker_name):
        if checker_name in self.__checkers:
            return self.__checkers[checker_name]
        else:
            return None
