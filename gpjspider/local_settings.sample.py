# -*- coding: utf-8 -*-

DEBUG = True

ITEM_PIPELINES = {
    'gpjspider.pipelines.save_to_db.DebugPipeline': 998,
}

DOWNLOADER_MIDDLEWARES = {
    'gpjspider.downloaders.SeleniumDownloader': 110,
    'gpjspider.downloaders.CurlDownloader': 119,
}

MYSQL_SQLALCHEMY_URL = {
    'drivername': 'mysql+mysqldb',
    'username': 'pingjia',
    'password': 'De32wsxc',
    # 'host': '101.251.105.186',
    'host': '211.149.206.212',
    'port': '3306',
    'database': 'pingjia',
    'query': {'charset': 'utf8'},
    #  mysql timeout 为 600，pool_recycle为create_engine的参数，不属于 URL。
    'pool_recycle': 550
}
