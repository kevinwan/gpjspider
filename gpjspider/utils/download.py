#-*- coding:utf-8 -*-
"""
从网上下载一个文件
"""
import os
import hashlib
import requests


def download_file(file_url):
    """
    todo: 还很不健壮

    从网上下载一个文件，返回临时文件路径
    """
    try:
        response = requests.get(file_url, headers={'Referer': file_url})
    except:
        return ''
    if response.status_code != 200:
        return ''

    key = '{0}.jpg'.format(hashlib.sha1(file_url).hexdigest())
    tmp_file = '/tmp/'+key
    with open(tmp_file, 'wb') as fp:
        fp.write(response.content)
        fp.flush()
    response.close()
    return tmp_file


def download_img_file(img_url):
    """
    todo: 需要判断文件 mime
    """
    tmp_file = download_file(img_url)
    if os.path.isfile(tmp_file):
        return tmp_file
    else:
        return ''
