# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER, SOURCE_TYPE_MANUFACTURER, SOURCE_TYPE_ODEALER

def model_slug(values):
    if isinstance(values, str):
        return values
    model = values[1][:-1]
    brand = values[0][:-1]
    if brand in model:
        model = model.lstrip(brand)
    return model.replace(' ', '')


def quality_service(value):
    import re
    if value:
        if re.search(ur".*[退修换保]+.*", value):
            return value
        if value.find('presur_ico') != -1:
            return u'无重大事故，无火烧，无水泡; 如若不符，15天全额包退，原厂质保'

        return u'无重大事故，无火烧，无水泡; 如若不符，15天全额包退'


# def is_certifield_car(value):
#     return True if value else False


def source_type(value):
    st = SOURCE_TYPE_ODEALER
    if isinstance(value, dict):
        item = value
        if item['is_certifield_car']:
            st = SOURCE_TYPE_MANUFACTURER if u'原厂质保' in item['quality_service'] else SOURCE_TYPE_SELLER
    return st

    # if isinstance(value, int):
    #     return value

    # if 'sell_ico' in value or 'promise_ico' in value:
    #     return SOURCE_TYPE_SELLER
    # elif value.find('presur_ico') != -1:
    #     return SOURCE_TYPE_MANUFACTURER
