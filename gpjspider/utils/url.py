# -*- coding: utf-8 -*-
"""
处理与 url 相关的函数
"""
from urlparse import urlparse


def get_domain(url):
    """
    获取 url 对应的域名

    如果 url 不完整，或任何未处理异常，返回"";
    - 返回的域名不包含端口号
    - 返回的域名不包含www，其他情况包含主机名
    """
    domain = ''
    url_st = urlparse(url)
    if ':' in url_st.netloc:
        domain = url_st.netloc.split(':')[0]
    else:
        domain = url_st.netloc
    _ = domain.split('.')
    domain = '.'.join(_[1:])
    if 'www' in domain:
        domain = domain.strip('www.')
    return domain
