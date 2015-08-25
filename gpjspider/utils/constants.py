#-*- coding:utf-8 -*-

#=============================================================================
# 变速箱类型
#=============================================================================
CONTROL_MODE_MANUAL = u'手动'
CONTROL_MODE_AUTOMATIC = u'自动'
CONTROL_MODE_MANUAL_AUTOMATIC = u'手自一体'

LIST_PAGE_PRIORITY = 5

#=============================================================================
# 车源类型
#=============================================================================
# 老爬虫车源
SOURCE_TYPE_OLD_SPIDER = 1
# 商家优质车  dealer
SOURCE_TYPE_SELLER = 2
# 厂商认证车  cpo
SOURCE_TYPE_MANUFACTURER = 3
# 个人来源  personal
SOURCE_TYPE_GONGPINGJIA = 4
# 一般商家车源    odealer
SOURCE_TYPE_ODEALER = 5


#=============================================================================
# 七牛文件上传 bucket 定义
#=============================================================================
QINIU_IMG_BUCKET = 'gongpingjia'



REDIS_DUP_SIG_KEY='dup_car_sig_%s'
REDIS_DUP_STAT_KEY='dup_car_stat'
REDIS_DUP_CHECKED_KEY='dup_car_checked'
REDIS_DUP_CACHE_OPEN_PRODUCT_SOURCE=False

TRADE_CAR_ALIVE_DAYS = 7

CLEAN_ITEM_HOUR_LIMIT=3# 
#during import we increase the time range
#CLEAN_ITEM_HOUR_LIMIT=30*2*24 #

USE_CELERY_TO_SAVE_CARSOURCE=False