# -*- coding: utf-8 -*-
"""
抓取百度上的热度
"""
import re
from decimal import Decimal
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BaiduHotItem
import urlparse
from datetime import datetime
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

DEBUG_SPIDER=False
# DEBUG_SPIDER=True

class BaiduHot(scrapy.Spider):
    name = "baidu_hot"
    domain='top.baidu.com'
    allowed_domains = ["baidu.com"]
    start_urls = (
        'http://top.baidu.com/category?c=18',
         # 'http://top.baidu.com/buzz?b=420&c=18',
    )
    _incr_enabled=False
    update=False
    only_sync_data=False

    def __init__(self, name=None, **kwargs):
        super(BaiduHot, self).__init__(name=name, **kwargs)
        self.the_date = datetime.now().strftime('%Y-%m-%d')
        dispatcher.connect(self.on_spider_closed, signals.spider_closed)
        dispatcher.connect(self.on_spider_opened, signals.spider_opened)

    def on_spider_opened(self, spider):
        if spider is not self:
            return
        from gpjspider.utils import get_mysql_connect
        session = get_mysql_connect()()
        from gpjspider.models.BaiduHot import BaiduHot as BaiduHotModel
        today_crawled_cnt = session.query(BaiduHotModel).filter_by(the_date=self.the_date).count()
        self.log(u'今日抓取数量:{0}'.format(today_crawled_cnt))
        if today_crawled_cnt>0:
            self.log(u'今日已经抓取过，本次只更新数据')
            self.log(u'如果需要重新抓取，清运行下面的脚本清理抓取记录后进行')
            self.only_sync_data = True
            sql='delete FROM baidu_hot_source where the_date="%s"' % self.the_date
            self.log(sql)
            if DEBUG_SPIDER:
                self.only_sync_data = False
                session.execute(sql)
        if DEBUG_SPIDER:
            session.execute('delete FROM open_cat_dic where domain="top.baidu.com"')
            session.execute('truncate table baidu_hot_source')

    def on_spider_closed(self, spider, reason):
        if spider is not self:
            return
        if not 'finished'==reason:
            self.log('spider not finished, do not convert')
        from gpjspider.models.BaiduHot import BaiduHot
        from gpjspider.models.product import Category,CategoryDict
        from gpjspider.utils import get_mysql_connect
        import pinyin
        session = get_mysql_connect()()

        default_parent = dict(
            domain=self.domain,
            name='未知',
            slug="Unknown",
            parent=None
        )
        if not session.query(CategoryDict).filter_by(**default_parent).count():
            category_dict = CategoryDict(url=self.start_urls[0], status='A', **default_parent)
            session.add(category_dict)
            session.commit()
        session.execute('update open_category set score=0 where 1=1')
        for row in session.query(BaiduHot).filter_by(the_date=self.the_date).yield_per(100):
            # self.log(u'updating {0} to score {1}'.format(row.keyword, row.score))
            name = row.keyword
            if row.is_brand:
                parent=None
                category_dict=session.query(CategoryDict).filter_by(
                    domain=self.domain,
                    name=name,
                    status='M',
                    parent=parent
                ).first()
                if category_dict is not None:
                    session.query(Category).filter_by(name=category_dict.global_name).update(dict(score=row.score), synchronize_session=False)
                else:
                    if not session.query(CategoryDict).filter_by(
                        domain=self.domain,
                        name=name,
                        # status='M',
                        parent=parent
                    ).count():# 不要反复建立待匹配的项目
                        slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9-_]', '-',  pinyin.get(name))).strip('-')
                        open_category= session.query(Category).filter_by(name=name).first()
                        cate_dict_item=dict(
                            domain=self.domain,
                            name=name,
                            slug=slug,
                            status='A',
                            # source_id=0,
                            url=row.url,
                            parent=parent,
                        )
                        matched=False
                        if open_category is not None:
                            cate_dict_item['global_name']=open_category.name
                            cate_dict_item['global_slug']=open_category.slug
                            cate_dict_item['status'] = 'M'
                            matched=True
                        category_dict = CategoryDict(**cate_dict_item)
                        session.add(category_dict)
                        session.commit()
                        if matched:
                            session.query(Category).filter_by(name=category_dict.global_name).update(dict(score=row.score), synchronize_session=False)
            else:
                parent='未知'
                category_dict=session.query(CategoryDict).filter_by(
                    domain=self.domain,
                    name=name,
                    status='M',
                    parent=parent,
                ).first()
                if category_dict is not None:
                    session.query(Category).filter_by(name=category_dict.global_name).update(dict(score=row.score), synchronize_session=False)
                else:
                    if not session.query(CategoryDict).filter_by(
                        domain=self.domain,
                        name=name,
                        # status='M',
                        parent=parent
                    ).count():# 不要反复建立待匹配的项目
                        slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9-_]', '-',  pinyin.get(name))).strip('-')
                        category_dict = CategoryDict(
                            domain=self.domain,
                            slug=slug,
                            name=name,
                            status='A',
                            # source_id=0,
                            url=row.url,
                            parent=parent,
                        )
                        session.add(category_dict)
        session.commit()
        self.log('scores updated to open_category!')

    def parse(self, response):
        """
        """
        g = re.compile(r'/(\d+)/')
        i = 0
        rule = '//div[@id="flist"]/div[@class="hblock"]/ul/li/a[@href]/@href'
        index_urls = response.xpath(rule)
        if not index_urls:
            self.log(u'基本规则失效:{0}'.format(rule), log.ERROR)
            yield None
            return

        if self.only_sync_data:
            self.log('只更新数据，不抓取')
            yield None
            return

        for index_url_xp in index_urls:
            index_url = index_url_xp.extract().strip()
            if '&c=18' in index_url and 'buzz' in index_url:
                real_url = urlparse.urljoin(response.url, index_url)
                self.log(u'fetching indexes from url:{0}'.format(real_url))
                yield Request(real_url, callback=self.parse_index, dont_filter=True)
                # if DEBUG_SPIDER:
                #     break

    def parse_index(self, response):
        """
        """
        self.log(u'解析指数 {0}'.format(response.url))
        rule = '//table[@class="list-table"]/tr'
        rows = response.xpath(rule)
        if not rows:
            self.log(u'基本规则失效:{0}'.format(rule), log.ERROR)
            yield None

        is_brand=0
        try:
            page_title = response.xpath('//div[@class="top-title"]/h2/text()').extract()[0]
            if u'汽车品牌' in page_title:
                is_brand=1
                self.log('当前页是汽车品牌页')
        except Exception as e:
            self.log("当前页不是汽车品牌页或者解析出错")
            self.log(e.message, log.ERROR)

        for row_xp in rows:
            if row_xp.xpath('td[@class="first"]'):
                if 1:
                    idx = row_xp.xpath('td[@class="first"]/span/text()').extract()
                    keyword = row_xp.xpath('td[@class="keyword"]/a[@class="list-title"]/text()').extract()
                    score = row_xp.xpath('td[@class="last"]/span/text()').extract()

                    item = BaiduHotItem()
                    item['score']=score[0]
                    item['keyword']=keyword[0]
                    item['domain']=self.domain
                    item['is_brand']=is_brand
                    item['url']=response.url
                    item['the_date'] = self.the_date
                    yield  item
