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


PHONE_OCR_BLACKLIST = (
    ('S', 'www.ganji.com'),
    #('S', 'used.xcar.com.cn'),
    ('R', '^[^\.]+\.ganji\.com$'),
)

REDIS_DUP_SIG_KEY='dup_car_sig_%s'
REDIS_DUP_STAT_KEY='dup_car_stat'
REDIS_DUP_CHECKED_KEY='dup_car_checked'
REDIS_DUP_CACHE_OPEN_PRODUCT_SOURCE=False

TRADE_CAR_ALIVE_DAYS = 7

CLEAN_ITEM_HOUR_LIMIT=3# 
#during import we increase the time range
CLEAN_ITEM_HOUR_LIMIT=30*2*24 #
CLEAN_ITEM_HOUR_LIMIT=10
CLEAN_STATUS='Y' #
# if it is not 0, will use as min id
CLEAN_MIN_ID=0
CLEAN_MAX_ID=0
CLEAN_DOMAIN=''
USE_CELERY_TO_SAVE_CARSOURCE=True
#USE_CELERY_TO_SAVE_CARSOURCE=False
SLEEP_BETWEEN_BATCH=1
SLEEP_BETWEEN_DELAY=0.2
# when we need to clean old needed status items, use the following criteria
if 0:
    CLEAN_STATUS=','.join([
        '_',
        'E',
        'I',
        '-model_slug',
        '-model_slug2',
        '-model_slug3',
    ])
try:
    from .local_constants import *
except ImportError:
    pass
