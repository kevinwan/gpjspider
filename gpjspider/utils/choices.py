#-*- coding:utf-8 -*-
from . import constants

# 变速器 choices
CONTROL_MODE_CHOICES = (
    (constants.CONTROL_MODE_MANUAL, u'手动'),
    (constants.CONTROL_MODE_AUTOMATIC, u'自动'),
    (constants.CONTROL_MODE_MANUAL_AUTOMATIC, u'手自一体')
)


# 车源类型 choices
SOURCE_TYPE_CHOICES = (
    (constants.SOURCE_TYPE_OLD_SPIDER, u'老爬虫车源'),  # 默认
    (constants.SOURCE_TYPE_SELLER, u'商家优质车'),
    (constants.SOURCE_TYPE_MANUFACTURER, u'厂商认证车'),
    (constants.SOURCE_TYPE_GONGPINGJIA, u'个人来源'),
)
