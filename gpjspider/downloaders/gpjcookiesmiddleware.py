# -*- coding: utf-8 -*-
"""
scrapy提供的 cookie 机制是把 server 带回的 cookie 再发送出去。

实际情况是，对不同的 url，要使用不同的 cookie。所以需要进行扩展。

本类完成的功能：
  在 rule 的 url 配置中，增加一个 cookie_function，负责生成url需要使用的cookie。
"""

from scrapy.contrib.downloadermiddleware.cookies import CookiesMiddleware


class GPJCookiesMiddleware(CookiesMiddleware):
    """
    """
    def process_request(self, request, spider):
        if request.meta.get('dont_merge_cookies', False):
            return

        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        cookies = self._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)

        # set Cookie header
        request.headers.pop('Cookie', None)
        jar.add_cookie_header(request)
        self._debug_cookie(request, spider)
