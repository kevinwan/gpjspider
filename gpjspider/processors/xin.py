# -*- coding: utf-8 -*-


def transfer_owner(value):
    if u'一手车' in value:
        return 0
    if u'次' in value:
        value = value.strip(u' 次')
        try:
            value = int(value)
        except:
            pass
    return value


def quality_service(value):
    if value == u'无':
        return ''
    else:
        return u''.join([
            u'通过无事故承诺的好车，无重大事故，无火烧，无水淹',
            u'如若不符，15天全额包退',
        ])


def is_certifield_car(value):
    return value


def volume(value):
    """
    例子：
    1. 二手奥迪 A4L 2013款 2.0T 自动 35TFSI标准型二手车 - 优信二手车
    """
    a = value.strip().split(' ')
    return a[3]


def control(value):
    """
    例子：
    1. 二手奥迪 A4L 2013款 2.0T 自动 35TFSI标准型二手车 - 优信二手车
    """
    a = value.strip().split(' ')
    return a[4]