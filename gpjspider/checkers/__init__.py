# -*- coding: utf-8 -*-
"""
定义各种规则检查类
"""
from gpjspider.utils.path import import_rule


class DefaultRuleChecker(object):
    """
    """
    name = 'default_checker'

    def __init__(self, rule_name):
        """
        """
        self.__rule_name = rule_name
        # print rule_name
        # import pdb
        # pdb.set_trace()
        self.rule = import_rule(rule_name)
        # self.rule = import_rule(self.__rule_name)
        if not self.rule:
            raise ValueError('todo')

    def check(self):
        """
        子类继承时实现
        """
        print('checkcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheck')
        print(unicode(self.rule))
        return self.rule


from gpjspider.checkers.manage import CheckerManager
