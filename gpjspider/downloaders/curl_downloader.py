# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from scrapy.http import HtmlResponse
# import pdb


def visit(url):
    p = Popen('curl %r' % url, shell=True, stdout=PIPE, stderr=PIPE)
    return p.communicate()[0]


class CurlDownloader(object):

    def process_request(self, request, spider):
        if request.meta.get("use_curl"):
            url = request.url
            data = visit(url)
            data = data.strip('()')
            # pdb.set_trace()
            # print data
            return HtmlResponse(url, body=data, encoding='utf-8')
