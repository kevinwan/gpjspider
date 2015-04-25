# -*- coding: utf-8 -*-

from importlib import import_module


def import_object(object_path):
    """
    format: AAA.BBB.ccc
    AAA.BBB是模块路径
    ccc 是对象
    """
    module, object_name = object_path.rsplit('.', 1)
    try:
        m = import_module(module)
    except ImportError:
        return None
    else:
        try:
            object_object = getattr(m, object_name)
        except:
            return None
        else:
            return object_object


def import_rule_function(rule_function):
    """
    format: AAA.BBB.ccc:arg1, arg2 ...
    AAA.BBB是模块路径
    ccc 是函数名
    : 之后是参数，只支持普通参数
    """
    processor_path = 'gpjspider.rule_functions.' + rule_function
    return import_object(processor_path)


def import_processor(processor_path):
    """
    format: AAA.BBB.ccc:arg1, arg2 ...
    AAA.BBB是模块路径
    ccc 是函数名
    : 之后是参数，只支持普通参数
    """
    processor_path = 'gpjspider.processors.' + processor_path
    return import_object(processor_path)


def import_item(item_class):
    """
    format: AAA.BBB.ccc:arg1, arg2 ...
    AAA.BBB是模块路径
    ccc 是函数名
    : 之后是参数，只支持普通参数
    """
    processor_path = 'gpjspider.items.' + item_class
    return import_object(processor_path)


def import_rule(rule_name):
    """
    @todo   如果不存在？
    """
    rule_path = 'gpjspider.rules.' + rule_name + '.rule'
    rule = import_object(rule_path)
    return rule


def import_update_rule(rule_name):
    """
    导入更新规则
    """
    rule_path = 'gpjspider.rules.update.' + rule_name + '.rule'
    rule = import_object(rule_path)
    return rule


def import_incr_rule(rule_name):
    """
    导入增量规则
    """
    rule_path = 'gpjspider.rules.incr.' + rule_name + '.rule'
    rule = import_object(rule_path)
    return rule


def import_full_rule(rule_name):
    """
    导入增量规则
    """
    rule_path = 'gpjspider.rules.full.' + rule_name + '.rule'
    rule = import_object(rule_path)
    return rule
