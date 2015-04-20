# -*- coding:utf-8 -*-
"""
需要 qiniu 7.0.3
"""
from __future__ import absolute_import
import os
import hashlib
from qiniu import Auth, put_file


class QiniuStorageService(object):
    """
    七牛云存储服务，需要的配置项：
    access_key
    secret_key
    bucket
    """
    def __init__(self, access_key, secret_key, bucket):
        """
        """
        self.__secret_key = secret_key
        self.__access_key = access_key
        self.__bucket = bucket
        self.__img_prefix = 'img'
        self.__auth = Auth(self.__access_key, self.__secret_key)

    def upload_images(self, image_path, delete_on_sucess=True):
        """
        """
        token = self.__auth.upload_token(self.__bucket)
        key = self.__img_prefix + '/' + hashlib.sha1(image_path).hexdigest()
        ret, info = put_file(token, key, image_path)
        if ret:
            if delete_on_sucess:
                try:
                    os.remove(image_path)
                except:
                    pass
        return ret, info

    def upload_file(self, file_path, delete_on_sucess=True):
        """
        """
        token = self.__auth.upload_token(self.__bucket)
        key = hashlib.sha1(file_path).hexdigest()
        ret, info = put_file(token, key, file_path)
        if ret:
            if delete_on_sucess:
                try:
                    os.remove(file_path)
                except:
                    pass
        return ret, info
