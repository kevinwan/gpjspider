# -*- coding: utf-8 -*-
"""
上传优质二手车图片到七牛
"""
from __future__ import absolute_import
import os
from PIL import Image
from celery.utils.log import get_task_logger
from gpjspider.utils.storage.qiniu import QiniuStorageService
from gpjspider.utils.download import download_file
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from gpjspider.utils.constants import QINIU_IMG_BUCKET


@app.task(name="batch_upload_to_qiniu", bind=True, base=GPJSpiderTask)
def batch_upload_to_qiniu(self, file_urls, qiniu_bucket=None):
    """
    """
    logger = get_task_logger('batch_upload_to_qiniu')
    logger.info(u'批量上传{0}到七牛'.format(file_urls))
    qiniu_bucket = qiniu_bucket if qiniu_bucket else self.app.conf.QINIU_BUCKET
    qiniu_store = QiniuStorageService(
        self.app.conf.QINIU_ACCESS_KEY,
        self.app.conf.QINIU_SECRET_KEY,
        qiniu_bucket
    )
    ret = []
    for file_url in file_urls:
        tmp_file = download_file(file_url)
        if not tmp_file:
            logger.error(u'下载文件失败:{0}'.format(file_url))
            continue
        logger.info(u'下载文件成功:{0}'.format(tmp_file))

        if QINIU_IMG_BUCKET == qiniu_bucket:
            r = __upload_img_file(qiniu_store, tmp_file, file_url, logger)
        else:
            r = __upload_file(qiniu_store, tmp_file, file_url, logger)
        if r:
            ret.append(r)
        else:
            logger.error(u'上传{0}失败'.format(file_url))
    return ret


@app.task(name="upload_to_qiniu", bind=True, base=GPJSpiderTask)
def upload_to_qiniu(self, file_url, qiniu_bucket=None):
    """
    """
    logger = get_task_logger('upload_to_qiniu')
    logger.info(u'上传{0}到七牛'.format(file_url))
    tmp_file = download_file(file_url)
    if not tmp_file:
        logger.error(u'下载文件失败:{0}'.format(file_url))
        return

    logger.info(u'下载文件成功:{0}'.format(tmp_file))
    qiniu_bucket = qiniu_bucket if qiniu_bucket else self.app.conf.QINIU_BUCKET
    qiniu_store = QiniuStorageService(
        self.app.conf.QINIU_ACCESS_KEY,
        self.app.conf.QINIU_SECRET_KEY,
        qiniu_bucket
    )
    if QINIU_IMG_BUCKET == qiniu_bucket:
        return __upload_img_file(qiniu_store, tmp_file, file_url, logger)
    else:
        return __upload_file(qiniu_store, tmp_file, file_url, logger)


def __upload_file(qiniu_store, tmp_file, file_url, logger):
    """
    默认的上传
    """
    ret, info = qiniu_store.upload_file(tmp_file, delete_on_sucess=True)
    if ret:
        logger.info(u'上传{0}到七牛:成功'.format(file_url))
        return ret['key']
    else:
        logger.info(u'上传{0}到七牛:失败'.format(file_url))
        return None


def __upload_img_file(qiniu_store, tmp_file, file_url, logger):
    """
    都转换成 jpg
    """
    new_file_path = tmp_file + '.jpg'
    try:
        image_obj = Image.open(tmp_file)
        image_obj.save(new_file_path)
    finally:
        # 不管成功与否，删除临时文件
        os.remove(tmp_file)
    if not os.path.isfile(new_file_path):
        logger.error(u'PIL转换图片{0}失败'.format(file_url))
        return ''
    ret, info = qiniu_store.upload_images(new_file_path, delete_on_sucess=True)
    if ret:
        logger.info(u'上传{0}到七牛:成功'.format(file_url))
        return ret['key']
    else:
        logger.info(u'上传{0}到七牛:失败:{1}'.format(file_url, unicode(info)))
        return None
