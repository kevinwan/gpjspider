# -*- coding: utf-8 -*-
"""
专属优车诚品的 processor
"""


def maintenance_record(value):
    """
    """
    return u'是' if value == '1' else u'否'


def transfer_owner(value):
    """
    """
    value = value.strip().strip(u'次')
    try:
        value = int(value)
    except:
        value = 0
    return value


def examine_insurance(value):
    """
    例：
    2016年04月
    """
    return value.replace(u'年', u'-').replace(u'月', u'')


def status(value):
    if value == u'<body>\r\nerror\r\n\r\n\r\n</body>':
        return 'Q'
    return 'Y'
