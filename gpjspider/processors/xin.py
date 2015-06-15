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
    import re

    if value:
        if re.search(ur".*[退修换保]+.*", value):
            return value
        if value.find('presur_ico') != -1:
            return u'无重大事故，无火烧，无水泡; 如若不符，15天全额包退，原厂质保'

        return u'无重大事故，无火烧，无水泡; 如若不符，15天全额包退'


def is_certifield_car(value):
    if value:
        return True

    return False


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


def source_type(value):
    from gpjspider.utils.constants import SOURCE_TYPE_SELLER, SOURCE_TYPE_ODEALER, SOURCE_TYPE_MANUFACTURER

    if isinstance(value, int):
        return value

    if value.find('sell_ico') != -1 or value.find('promise_ico') != -1:
        return SOURCE_TYPE_SELLER

    if value.find('presur_ico') != -1:
        return SOURCE_TYPE_MANUFACTURER