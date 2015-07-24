"""
Domain Depth Spider Middleware
See documentation in docs/topics/spider-middleware.rst
"""

from scrapy import log
from scrapy.http import Request
# import tldextract

class DomainDepthMiddleware(object):
    def __init__(self, domain_depths, default_depth, crawler=None):
        self.crawler = crawler
        self.domain_depths = domain_depths
        self.default_depth = default_depth
        self.init = True
        self.maxdepth = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        domain_depths = settings.getdict('DOMAIN_DEPTHS', default={})
        default_depth = settings.getint('DEPTH_LIMIT', 3)

        return cls(domain_depths, default_depth, crawler)

    def get_max_depth(self, spider):
        if not self.maxdepth:
            self.maxdepth = self.domain_depths.get(spider.domain, self.default_depth)
        return self.maxdepth

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                # get max depth per domain
                # domain = spider.domain
                # maxdepth = self.domain_depths.get(domain, self.default_depth)
                maxdepth = self.get_max_depth(spider)
                depth = response.meta.get('depth', 0) + 1
                request.meta['depth'] = depth

                if maxdepth and depth > maxdepth:
                    log.msg(format="Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
                            level=log.DEBUG, spider=spider,
                            maxdepth=maxdepth, requrl=request.url)
                    return False
            return True
        if self.init:

            if hasattr(spider, '_incr_enabled') and not spider._incr_enabled:
                settings = self.crawler.settings
                self.domain_depths = settings.getdict('DOMAIN_FULL_DEPTHS', default={})
                self.default_depth = settings.getint('DEPTH_FULL_LIMIT', 5)
            if 'depth' not in response.meta:
                response.meta['depth'] = 0
            self.init = False

        return (r for r in result or () if _filter(r))

    # def __init__(self, maxdepth, stats=None, verbose_stats=False, prio=1):
    #     self.maxdepth = maxdepth
    #     self.stats = stats
    #     self.verbose_stats = verbose_stats
    #     self.prio = prio

    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     maxdepth = settings.getint('DEPTH_LIMIT')
    #     verbose = settings.getbool('DEPTH_STATS_VERBOSE')
    #     prio = settings.getint('DEPTH_PRIORITY')
    #     return cls(maxdepth, crawler.stats, verbose, prio)

    # def process_spider_output(self, response, result, spider):
    #     def _filter(request):
    #         if isinstance(request, Request):
    #             depth = response.meta['depth'] + 1
    #             request.meta['depth'] = depth
    #             if self.prio:
    #                 request.priority -= depth * self.prio
    #             if self.maxdepth and depth > self.maxdepth:
    #                 log.msg(format="Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
    #                         level=log.DEBUG, spider=spider,
    #                         maxdepth=self.maxdepth, requrl=request.url)
    #                 return False
    #             elif self.stats:
    #                 if self.verbose_stats:
    #                     self.stats.inc_value('request_depth_count/%s' % depth, spider=spider)
    #                 self.stats.max_value('request_depth_max', depth, spider=spider)
    #         return True

    #     # base case (depth=0)
    #     if self.stats and 'depth' not in response.meta:
    #         response.meta['depth'] = 0
    #         if self.verbose_stats:
    #             self.stats.inc_value('request_depth_count/0', spider=spider)

    #     return (r for r in result or () if _filter(r))