# -*- coding: utf-8 -*-
"""
提取 url 规则：

"""
import pickle
import inspect
from prettyprint import pp_str
from sqlalchemy.exc import IntegrityError
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem
from gpjspider.utils import get_redis_cluster, get_mysql_connect
from gpjspider.models.requests import RequestModel
from gpjspider.utils.path import import_rule_function, import_item
from gpjspider.utils.path import import_processor
from gpjspider.checkers import CheckerManager
from gpjspider.checkers.constants import HIGH_QUALITY_RULE_CHECKER_NAME
from gpjspider.utils.constants import LIST_PAGE_PRIORITY

import re
import json
from .utils import *
from gpjspider.utils import get_mysql_cursor
import ipdb, pdb
import math
from gpjspider.models import UsedCar
from gpjspider.tasks.clean.usedcars import clean
import urlparse
from datetime import datetime, timedelta


def debug():
    pdb.set_trace()


class GPJBaseSpider(scrapy.Spider):
    default_max_page = 10000
    full_page = 600
    # full_page = 30
    # full_page = 20
    full_page = 12
    incr_page = 5
    incr_page = 3
    # incr_page = 0
    # full_page = 60
    # incr_page = 30
    _incr_enabled = False
    _is_export = False

    def __init__(self, rule_name, update=False, dealer=False, checker_name=None, *args, **kwargs):
        super(GPJBaseSpider, self).__init__(*args, **kwargs)
        self.update = update
        self.with_dealer = dealer
        self.__rule_path = rule_name
        self.website_rule = {}
        self.domain = None
        self.checker_manager = CheckerManager()
        if not checker_name:
            checker_name = HIGH_QUALITY_RULE_CHECKER_NAME

        self.__checker_name = checker_name
        self.checker_class = self.checker_manager.get_checker(checker_name)
        self.checker = self.checker_class(rule_name)
        rule = self.website_rule = self.checker.check()
        self.setup_rule(rule_name)
        self.page_urls = set()
        self.detail_urls = set()
        self.page_rule = None
        self.max_page = self.default_max_page
        self.new = None
        if not self.website_rule:
            raise ValueError('TODO')
        for attr in 'domain dealer'.split():
            setattr(self, attr, rule.get(attr))
        self._is_export and self.export_incr_rule(rule_name)
        self.Session = get_mysql_connect()

    def export_incr_rule(self, rule_name):
        rule_name = rule_name.split('.')[-1]
        with open('gpjspider/rules/incr/%s.json' % rule_name, 'w') as fp:
            data = json.dumps(self.website_rule)
            fp.write(data)

    def setup_rule(self, rule_name):
        pass

    def set_crawler(self, crawler):
        super(GPJBaseSpider, self).set_crawler(crawler)
        self.proxy_ips = self.get_proxy_ips()

    def log(self, msg, level=log.DEBUG, **kw):
        super(GPJBaseSpider, self).log(msg.encode('utf-8'), level=level, **kw)

    def get_proxy_ips(self):
        redis = get_redis_cluster()
        s = redis.smembers('valid_proxy_ips')
        # self.log(u'all proxies: {0}'.format(s))
        return s and list(s) or []

    def start_requests(self):
        if 'start_urls' in self.website_rule:
            start_urls = self.website_rule['start_urls']
            if self.update:
                psize = 5
                session = self.Session()
                query = session.query(UsedCar.id, UsedCar.url).filter_by(domain=self.domain, status='u')
                items = query.limit(psize).all()
                session.close()
                while items:
                    for item in items:
                        yield Request(item.url, meta=dict(id=item.id), callback=self.parse_detail, dont_filter=True)
                    session = self.Session()
                    query = session.query(UsedCar.id, UsedCar.url).filter_by(domain=self.domain, status='u')
                    items = query.limit(psize).all()
                    session.close()
                return
            elif self.with_dealer:
                psize = 20
                dealer = dict(callback=self.parse_list, dont_filter=True)
                dealer_url = self.dealer.pop('url')
                reg = None
                if 'regex' in self.dealer:
                    reg = self.dealer.pop('regex')

                dealer = dict(dealer, **self.dealer)
                session = self.Session()
                start_time = end_time = datetime.now()
                # end_time -= timedelta(hours=1)
                try:
                    delta = int(self.with_dealer)
                except:
                    delta = 0.5
                start_time -= timedelta(hours=delta * 4)
                query = session.query(UsedCar.company_url).filter(UsedCar.created_on >= start_time,
                    UsedCar.created_on < end_time).filter_by(domain=self.domain) \
                    .filter(UsedCar.company_url != None,
                        # UsedCar.city.in_([u'\u5317\u4eac', u'\u6210\u90fd', u'\u5357\u4eac']))\
                        UsedCar.city.in_(u'北京 成都 南京'.split()))\
                    .distinct()
                    # .filter(~UsedCar.company_url.in_([None, ''])).distinct()
                # print query.count()
                for item in query.yield_per(psize):
                    url = item.company_url
                    if reg:
                        match = re.findall(reg, url)
                        if match:
                            url = match[0]
                    yield Request(dealer_url % url, **dealer)
                session.close()
                return
        elif 'start_url_function' in self.website_rule:
            start_url_function = self.website_rule['start_url_function']
            start_urls = start_url_function(
                self.website_rule['start_url_template'], self
            )
        for start_url in start_urls:
            self.log(u'start request {0}'.format(start_url), log.INFO)
            self.page_urls.add(start_url)
            request = self.make_requests_from_url(start_url)
            # request.priority = LIST_PAGE_PRIORITY
            yield request


    def parse(self, response, my_name=None):
        step_rule = self.website_rule[my_name or 'parse']
        # self.test(response)
        detail_amount = 0
        delta = 0

        if 'replace' in step_rule:
            replace_rule = step_rule['replace']
            for rr in replace_rule:
                response = response.replace(**rr)
        if 'url' in step_rule:
            msg = u'try to get new urls from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['url'], response)
            size = len(requests)
            if size > 0:
                response.meta['depth'] = response.meta.get('depth', 0) - 1
                if size > 3:
                    delta -= 1
            # print response.meta['depth'], len(requests)
            for request in requests:
                self.log('start request {0}'.format(request.url))
                yield request
                detail_amount += 1
        if detail_amount > 0:
            # delta = int(math.ceil((detail_amount-1) / 6.0))# - 1
            delta += int(math.ceil(detail_amount / 6.0))
            # delta = int(math.ceil(detail_amount / 6.0)) - 1
            # delta = int(math.floor(detail_amount / 7.0))# - 1
            if detail_amount == size:
                if size > self.website_rule.get('per_page', 15) / 3:
                    delta += 1
                    if delta > 4:
                        delta = 4
            elif self._incr_enabled:
                delta += 1
        depth = response.meta.get('depth', 0) - delta
        _min = -12
        depth = depth if depth > _min else _min
        # print depth
        response.meta['depth'] = depth
        if 'list_url' in step_rule:
            msg = u'try to get new list urls from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['list_url'], response)
            # size = len(requests)
            # if size > 0:
            #     response.meta['depth'] = response.meta.get('depth', 0) - 1
            #     if size > 3:
            #         delta -= 1
            # print response.meta['depth'], len(requests)
            for request in requests:
                self.log('start list request {0}'.format(request.url))
                # ipdb.set_trace()
                yield request
                # detail_amount += 1
        page_rule = self.get_page_rule(step_rule)
        if page_rule:
            msg = u'try to get next page url from {0}'.format(response.url)
            self.log(msg)
            requests = self.get_requests(page_rule, response, detail_amount or step_rule)
            # if len(requests) > 10:
            # response.meta['depth'] += 1 #depth if  else depth
            for request in requests:
                url = request.url
                # request.priority = LIST_PAGE_PRIORITY
                self.log(u'start next request: {0}'.format(url))
                yield request

        if 'item' in step_rule:
            yield self.get_item(step_rule['item'], response)
        elif 'items' in step_rule:
            for item in self.get_items(step_rule['items'], response):
                yield item

    def get_page_rule(self, step_rule):
        if self.page_rule is None:
            self.page_rule = step_rule.get('incr_page_url', step_rule.get('next_page_url'))
        return self.page_rule

    def get_max_page(self, page_rule=None):
        if self.max_page >= self.default_max_page:
            rule = self.website_rule
            page_rule = self.get_page_rule(rule.get('parse_list', rule.get('parse')))
            url_no = len(self.page_urls)
            if self._incr_enabled:
                page = page_rule.get('incr_pageno', url_no > 8 and 1 or url_no > 1 and 3 or self.incr_page)
                # url_no = url_no > 40 and 40 or url_no
            else:
                page = page_rule.get('max_pagenum', self.full_page)
                #page = 31
            self.max_page = page * url_no
            # print self.max_page
        return self.max_page

    def parse_list(self, response):
        # self.test(response)
        return self.parse(response, 'parse_list')

    def test(self, response):
        print response.meta['depth'], response.url

    def parse_detail(self, response):
        """
        step rule中加入replace参数解决有些页面信息缺失或非utf-8编码问题
        """
        # self.test(response)
        import sys

        my_name = sys._getframe().f_code.co_name
        step_rule = self.website_rule[my_name]
        if 'replace' in step_rule:
            replace_rule = step_rule['replace']

            for rr in replace_rule:
                response = response.replace(**rr)

        if 'item' in step_rule:
            if self.update:
                cursor = self.get_cursor()
                cursor.execute('update open_product_source set status="Q" where id=%s;' % response.meta['id'])
                cursor.close()
            yield self.get_item(step_rule['item'], response)
            if self.update:
                cursor = self.get_cursor()
                cursor.execute('update open_product_source set status="B" where id=%s and status != "Q";' % response.meta['id'])
                cursor.close()
                # clean(response.meta['id'], response.meta['id'], [self.domain], 'B')
                print response.meta['id'], response.url, '\n************************************************'

    def get_requests(self, url_rule, response, step_rule=None):
        """
        支持 xpath  re  css  json  function
        excluded中的将会被排除
        """
        urls = set()
        meta_info = {}
        step_function = self.get_next_step(url_rule)
        if 'xpath' in url_rule:
            if isinstance(url_rule['xpath'], dict):
                func = url_rule['xpath'].get('function')
                if not func:
                    raise ValueError('need function in parse_rule.xpath')
                func_name = func.__name__
                self.log(u'try to get url and addition info from function {0}'.format(func_name))
                urls, meta_info = func(response, self)
            else:
                for rule in url_rule['xpath']:
                    _urls = set(response.xpath(rule).extract())
                    self.log(u'rule: {0}, urls: {1}'.format(rule, _urls))
                    urls |= _urls
        if 're' in url_rule:
            for rule in url_rule['re']:
                urls |= set(response.selector.re(rule))
        if 'css' in url_rule:
            for rule in url_rule['css']:
                urls |= set(response.css(rule).extract())
        if 'json' in url_rule:
            urls |= set([unicode(url) for url in self.get_json(response.body, url_rule['json'])])
        # if 'match' in url_rule:
        #     for url in urls:
        #         match = url_rule['match']:
        #         if ex_url in url:
        #             tmp_urls.add(url)
        #             break
        if urls:
            self.log(u'Got {0} Urls..'.format(len(urls)), log.DEBUG)
        tmp_urls = set()
        if 'contains' in url_rule:
            contains = url_rule['contains']
            contains = [contains] if isinstance(contains, str) else contains
            for url in urls:
                if not any([info in url for info in contains]):
                    tmp_urls.add(url)
        if 'excluded' in url_rule:
            for url in urls:
                for ex_url in url_rule['excluded']:
                    if ex_url in url:
                        tmp_urls.add(url)
                        break

        # pdb.set_trace()
        try:
            if 'regex' in url_rule:
                regex = url_rule['regex']
                if isinstance(regex, list):
                    flag = False
                    for reg in regex:
                        try:
                            match = re.findall(reg, value)
                            if match:
                                value = match[0]
                                flag = True
                                break
                        except Exception as e:
                            value = url_rule.get('regex_fail', value)
                            # flag = True
                            break
                    if not flag:
                        # value = url_rule.get('regex_not', value)
                        value = url_rule.get('regex_not')
                else:
                    try:
                        urls = [re.findall(regex, url)[0] for url in urls]
                    except Exception as e:
                        urls = url_rule.get('regex_fail', urls)
                        # print value
        except Exception as e:
            # print e
            pass
        finally:
            urls = set(urls)
        if tmp_urls:
            self.log(u'{0} Dups Urls..'.format(len(tmp_urls)), log.INFO)
        urls -= tmp_urls

        urls = self.format_urls(url_rule, urls, response.url, meta_info=meta_info)

        # 设置dont_filter比使用默认值优先级要高
        # 默认值是：如果 step 规则中有 item，则False；如果 step 规则中没有 item，则 True
        if 'dont_filter' in url_rule:
            dont_filter = url_rule['dont_filter']
        else:
            next_step = step_function.__name__
            if 'item' in self.website_rule[next_step] or next_step == 'parse_detail':
                dont_filter = False
            else:
                dont_filter = True

        ret_requests = []
        _url = response.url
        if 'function' in url_rule:
            func = url_rule.get('function')
            func_name = func.__name__

            self.log(u'try to get url from function {0}'.format(func_name))
            url_dicts = func(response, url_rule, self)
            for url_dict in url_dicts:
                if 'url' in url_dict:
                    url = url_dict.pop('url')
                    url = self.exec_processor(None, url_rule, url)
                    if url in self.page_urls:
                        continue
                else:
                    self.log(u'no url get from {0}'.format(url_dict))
                    continue
                # self.log(u'cookies is {0}'.format(pp_str(cookies)))
                if url_dict:
                    self.log(u'args is {0}'.format(url_dict))
                request = Request(
                    url, callback=step_function, dont_filter=dont_filter, **url_dict
                )
                ret_requests.append(request)
        else:
            urls = set([self.exec_processor(None, url_rule, url)
                        for url in urls])
            if dont_filter:
                urls -= self.page_urls
                for url in urls:
                    self.page_urls.add(url)
                # if step_rule:
                #     max_page = self.max_page
                #     pages = len(self.page_urls)
                # TODO: need opt
                #     if pages > max_page:
                #         self.log(
                #             'visit {0}/{1} pages before {2}'.format(pages, max_page, _url))
                #         return []
            else:
                urls -= self.detail_urls
                for url in urls:
                    self.detail_urls.add(url)
                # and self.domain != 'c.cheyipai.com':
                if urls and not self.update:
                    # max_page = self.get_max_page(url_rule)
                    max_page = 0
                    urls = self.clean_detail_urls(urls, _url, max_page)
                    # dont_filter = not self._incr_enabled
            for url in urls:
                meta = meta_info.get(url)
                # if meta:
                #     print meta
                request = Request(
                    url, callback=step_function, dont_filter=dont_filter, meta=meta)
                ret_requests.append(request)

        # if 'update' in url_rule and 'category' in url_rule:
        #     if url_rule['update']:
        #         try:
        #             self.save_request(ret_requests, url_rule['category'])
        #         except Exception as e:
        # self.log(u'Save request{0} failed', level=log.ERROR)
        #             self.log(str(e), level=log.ERROR)

        return ret_requests

    def clean_detail_urls(self, urls, url, max_page):
        # klass = UsedCar
        # res = session.query(klass).filter(klass.url.in_(urls)).values('url')
        query = "select url from open_product_source where url in ('%s')"
        cursor = self.get_cursor()
        res = cursor.execute(query % "','".join(urls)).fetchall()
        existed_urls = set([c.url for c in res])
        cursor.close()
        new_urls = urls - existed_urls
        new_no = len(new_urls)
        all_no = len(urls)
        # del_no = all_no - new_no
        if new_no:
            self.log(u'Found {0}/{1} items in {2}'.format(new_no, all_no, url))
        # elif del_no:
        #     self.log(u'Cleaned {0} Existed Urls..'.format(del_no), log.DEBUG)
        #     min_no = all_no / 3
        #     if new_no > all_no and all_no >= 5:
        #         max_page += 2.1
        #     elif new_no / 2 > min_no or new_no >= 20:
        #         max_page += 1.6
        #     elif new_no > min_no or new_no >= 8:
        #         max_page += 1.1
        # elif max_page > 30:
        #     max_page -= 0.7
        # self.max_page = max_page
        return new_urls

    def get_cursor(self):
        return get_mysql_cursor()

    def get_items(self, items_rule, response):
        """
        根据 field 规则获取响应数据items
        优先级: arg/xpath > key/json > default
        """
        nodes = []
        item_class = import_item(items_rule['class'])
        if 'xpath' in items_rule:
            nodes = response.xpath(items_rule['xpath'])
            if items_rule['is_json']:
                nodes = self.load_json(nodes.extract()[0])
        elif 'json' in items_rule:
            json_str = response.body
            nodes = self.get_json(json_str, items_rule['json'])
        res_url = response.url
        for item_node in nodes:
            item = item_class()
            item['domain'] = self.domain
            for field_name, field in items_rule['fields'].iteritems():
                values = None
                # is_global = field.get('global')
                # if is_global:
                #     values = locals().get(field_name)
                if 'arg' in field:
                    values = re.findall(
                        '[&\?]%s=([^&]*)' % field['arg'], res_url)[0]
                elif 'xpath' in field:
                    xpath = field['xpath']
                    res = response if xpath[0].startswith('//') else item_node
                    values = self.get_xpath(xpath, res)
                if values is None:
                    if 'key' in field:
                        values = item_node[field['key']]
                    elif 'json' in field:
                        values = self.get_json(response.body, field['json'])
                    if values is None:
                        if 'default' in field:
                            default = field['default']
                            try:
                                values = eval(default)
                            except:
                                values = default
                if values:
                    item[field_name] = values
                    item = self.exec_processor(field_name, field, item)
                    value = item[field_name]
                    if 'regex' in field:
                        try:
                            value = re.findall(field['regex'], value)[0]
                            # value = value and value[0] or field.get('regex_not')
                        except:
                            value = field.get('regex_fail', value)
                    if 'format' in field and not value.startswith('http'):
                        value = field['format'].format(value)
                    item[field_name] = value
                if field.get('required', False):
                    if field_name not in item:
                        m = u'{0} is required: {1}'.format(field_name, res_url)
                        raise DropItem(m)
                # if is_global and field_name not in locals():
                #     exec '%s = item[field_name]' % (field_name, )
            teardown_func = items_rule.get('teardown')
            if teardown_func:
                teardown_func = import_processor(teardown_func)
                if teardown_func:
                    teardown_func(item)
            yield item

    item_keys = [
        'url', 'meta', 'title', 'dmodel', 'description', 'city', 'city_slug', 'brand_slug', 'model_slug', 'model_url',
        'volume', 'year', 'month', 'mile', 'control', 'color', 'price_bn',
        'price', 'transfer_owner', 'car_application', 'mandatory_insurance', 'business_insurance', 'examine_insurance',
        'company_name', 'company_url', 'phone', 'contact', 'region', 'imgurls',
        'maintenance_record', 'maintenance_desc', 'quality_service', 'driving_license', 'invoice',
        'time', 'is_certifield_car', 'source_type', 'condition_level', 'condition_detail', 'status',
    ]

    def get_item(self, item_rule, response):
        """
        priority: xpath > json > css > str > function > default
        """
        item_cls = import_item(item_rule['class'])
        # item = dict(response.meta)
        item = dict(url=response.url)
        if 'id' in response.meta:
            item['id'] = response.meta['id']
        fields = item_rule['fields']
        for field in fields:
            if field in response.meta:
                item[field] = response.meta[field]
        meta_keys = set([])
        for key in response.meta.keys():
            if key.startswith('_'):
                item[key] = response.meta[key]
                meta_keys.add(key)
        item['domain'] = self.domain
        for field_name in item_rule.get('keys', self.item_keys):
            process_step = ''
            print_error = False
            have_rule = False
            field = fields.get(field_name)
            if not field:
                continue
            values = None
            if 'xpath' in field:
                have_rule = True
                rules = field['xpath']
                # if field_name == 'phone':
                    # ipdb.set_trace()
                if isinstance(rules, tuple):
                    values = self.get_xpath(rules, response)
                else:
                    values = []
                    for rule in rules:
                        values.extend(self.get_xpath([rule], response))
                if not values and not print_error and field['xpath']:
                    process_step = 'xpath'
                    print_error = True
            if not values:
                if 'json' in field:
                    have_rule = True
                    values = self.get_json(response.body, field['json'])
                    if not values and not print_error and field['json']:
                        process_step = 'json'
                        print_error = True
                if not values:
                    if 'css' in field:
                        have_rule = True
                        values = self.get_xpath(field['css'], response)
                        if not values and not print_error and field['css']:
                            process_step = 'css'
                            print_error = True
                    if not values:
                        if 're' in field:
                            have_rule = True
                            values = self.extract_str(field['re'], response)
                            if not values and not print_error and field['re']:
                                process_step = 're'
                                print_error = True
                        if not values:
                            if 'function' in field:
                                have_rule = True
                                func_name = field['function']['name']
                                func = import_rule_function(func_name)
                                if not func:
                                    f = field['function']
                                    m = u'{0} rule {1} error: {2}'.format(
                                        field_name, 'function', f)
                                    self.log(m, log.ERROR)
                                    continue
                                args = field['function'].get('args', tuple())
                                kwargs = field['function'].get('kwargs', {})
                                values = func(response, self, *args, **kwargs)
                                if not values and not print_error and field['function']:
                                    process_step = 'function'
                                    print_error = True
                            if not values:
                                if 'default' in field:
                                    have_rule = True
                                    value = field['default']
                                    if value == '{item}':
                                        values = item
                                    elif isinstance(value, basestring) and '%(' in value:
                                        try:
                                            value %= item
                                        except Exception as e:
                                            if 'default_fail' in field:
                                                value = field['default_fail']
                                        values = value
                                    elif isinstance(value, (list, tuple)):
                                        values = []
                                        for v in value:
                                            if '%(' in v:
                                                try:
                                                    v %= item
                                                except Exception as e:
                                                    if 'default_fail' in field:
                                                        v = field[
                                                            'default_fail']
                                            values.append(v)
                                    else:
                                        values = value

                                    item[field_name] = values
                                else:
                                    if not print_error:
                                        if not have_rule:
                                            m = u'field {0} missing rule'.format(
                                                field_name)
                                            self.log(m, log.WARNING)
                                        m = u'field {0} is NULL: {1}'.format(
                                            field_name, response.url)
                                        self.log(m, log.WARNING)
                                    else:
                                        self.rule_log_print(
                                            field_name, response.url, process_step, field)

            if values:
                print_error = False
                item[field_name] = values
                # 执行处理器
                processors = []
                if 'processors' in field:
                    processors = field['processors']
                    process_step = 'processors'
                # if field_name == 'model_slug':
                   # ipdb.set_trace()
                try:
                    if field_name in processors:
                        processors.remove(field_name)
                    it = self.exec_processor(field_name, field, item)
                    if isinstance(it, dict):
                        item = it
                except Exception as e:
                    print e
                    # value = value or None
                    # continue
                finally:
                    value = item[field_name]
                    value_old = value
                try:
                    if 'regex' in field:
                        regex = field['regex']
                        process_step = 'regex'
                        if isinstance(regex, list):
                            flag = False
                            for reg in regex:
                                try:
                                    match = re.findall(reg, value)
                                    if match:
                                        value = match[0]
                                        flag = True
                                        break
                                except Exception as e:
                                    value = field.get('regex_fail', value)
                                    break
                            if not flag:
                                value = field.get('regex_not')
                        else:
                            try:
                                value = re.findall(regex, value)[0]
                            except Exception as e:
                                value = field.get('regex_fail', value)
                        if not value and not print_error:
                            self.processors_log_print(
                                field_name, process_step, field, value_old, value)
                            print_error = True
                    value_old = value
                    if 'after' in field:
                        value = after(value, field['after'])
                        process_step = 'after'
                        if not value and not print_error:
                            m = u'{0} not found "{1}" in "{2}"'.format(
                                field_name,
                                field[process_step],
                                value_old
                            )
                            self.log(m, log.WARNING)
                    if 'before' in field:
                        value = before(value, field['before'])
                        process_step = 'before'
                        if not value and not print_error:
                            m = u'{0} not found "{1}" in "{2}"'.format(
                                field_name,
                                field[process_step],
                                value_old
                            )
                            self.log(m, log.WARNING)
                    if 'format' in field and not value.startswith('http') and value.startswith('/'):
                        fmt_rule = field['format']
                        if fmt_rule == True:
                            fmt_rule = response.url
                        elif isinstance(fmt_rule, str) and '%(' in fmt_rule:
                            fmt_rule %= dict(url=_url)
                        if '{0}' in fmt_rule:
                            value = fmt_rule.format(value)
                        if fmt_rule:
                            value = urlparse.urljoin(fmt_rule, value)
                        # ipdb.set_trace()
                except Exception as e:
                    print e
                    pass
                if field_name == item_rule.get('debug'):
                    pdb.set_trace()
                item[field_name] = self.exec_processor(None, field_name, value)

            # required判断
            if field_name not in item and field.get('required', False):
                m = u'{0} is required: {1}'.format(
                    field_name, response.url)
                raise DropItem(m)
        for key in meta_keys:
            if key in item:
                item.pop(key)
        return item_cls(item)

    def rule_log_print(self, field_name, url, process_step, field):
        if process_step in field:
            m = u'{0}\'s {1} "{2}" failed'.format(
                field_name,
                process_step,
                field[process_step]
            )
            self.log(m, log.ERROR)
        m = u'field {0} is NULL: {1}'.format(
            field_name, url)
        self.log(m, log.WARNING)

    def processors_log_print(self, field_name, process_step, field, value_old, value):
        m = u'{0}\'s {1} "{2}" failed'.format(
            field_name,
            process_step,
            field[process_step]
        )
        if value == value_old:
            m = m + u' - "{0}"'.format(value)
        else:
            m = m + u' - from "{0}" to "{1}"'.format(value_old, value)
        self.log(m, log.WARNING)

    def get_xpath(self, xpath_rules, response):
        for xpath_rule in xpath_rules:
            try:
                values = response.xpath(xpath_rule).extract()
                if values:
                    return values
            except Exception as e:
                print locals()
                print e
        return []

    def get_json(self, json_unicode, json_path):
        """
        处理一段 json 字符串
        """
        try:
            jso = self.load_json(json_unicode)
        except Exception as e:
            self.log(str(e), level=log.ERROR)
            return None
        else:
            return self.parse_json_path(json_path, jso)

    def load_json(self, json_unicode):
        return json.loads(json_unicode)

    def get_css(self, css_rules, response):
        for css_rule in css_rules:
            values = response.css(css_rule).extract()
            if values:
                return values
        return []

    def get_str(self, str_rules, response):
        for str_rule in str_rules:
            assert len(str_rule) == 2, 'str guize error'
            start_index = response.body.find(str_rule[0])
            if start_index == -1:
                continue
            start_index += len(str_rule[0])
            end_index = response.body.find(str_rule[1], start_index)
            if end_index == -1:
                continue
            return [response.body[start_index:end_index]]
        return []

    def extract_str(self, regx_rules, response):
        txt = response.body
        for regx_rule in regx_rules:
            match = re.findall(regx_rule, txt)
            if match:
                return match[0]
        return []

    def exec_processor(self, field_name, field_rule, item):
        """
        根据字段规则定义和当前 item，对此字段进行过滤，暂时不支持 processor参数
        """
        if isinstance(field_rule, dict):
            processors = field_rule.get('processors', ['first'])
        else:
            processors = [field_rule]
        for processor in processors:
            processor_func = import_processor(processor)
            if not processor_func:
                if field_name:
                    m = u'{0}\'s processor "{1}" not exist'.format(
                        field_name,
                        processor
                    )
                    self.log(m, log.WARNING)
                return item
            if field_name and field_name in item:
                item[field_name] = processor_func(item[field_name])
            else:
                item = processor_func(item)
        return item

    def parse_json_path(self, json_path, jsobject):
        """
        尝试解析 json 表达式
        - 表示  {}
        |表示[]
        每次以$#$分隔, 如  -data$#$|
        """
        steps = json_path.strip().split('$#$')
        while steps:
            step = steps.pop(0)
            if step[0] == '-':
                jsobject = jsobject[step[1:]]
            elif step[0] == '|':
                if step[1:].upper() == 'ALL':
                    values = []
                    for _jsobject in jsobject:
                        jsobject = self.parse_json_path(
                            '$#$'.join(steps), _jsobject
                        )
                        values.append(jsobject)
                    steps = []
                    jsobject = values
                else:
                    try:
                        index = int(step[1:].upper())
                    except:
                        pass
                    else:
                        jsobject = jsobject[index]
        return jsobject

    def get_next_step(self, url_rule):
        if not hasattr(self, url_rule['step']):
            s = pp_str(url_rule['step'])
            self.log(u'no url step configure：{0}'.format(s), level=log.ERROR)
            return None
        step = getattr(self, url_rule['step'])
        if not inspect.ismethod(step):
            n, cn = step.__name__, step.__class__.__name__
            self.log(u'object {0} is instance of {1}'.format(n, cn), level=log.WARNING)
            return None
        return step

    def format_urls(self, url_rule, urls, _url=None, meta_info=None):
        # if urls:
        #     self.log(u'got {0} urls'.format(urls))
        if 'format' not in url_rule:
            return urls
        # format_rule = url_rule['format'].replace('%(url)s', _url)
        format_rule = url_rule['format']
        if format_rule == True:
            format_rule = re.findall('(http://[^/]+)/?', _url)[0]
        elif isinstance(format_rule, str) and '%(' in format_rule:
            format_rule %= dict(url=_url)
        elif isinstance(format_rule, dict) and urls:
            url = list(urls)[0]
            # fmt_rule = None
            for k, v in format_rule.items():
                if url.startswith(k):
                    format_rule = v
                    break
            if '%(' in format_rule:
                # format_rule %= dict(url=_url)
                format_rule = _url
            # format_rule = _url
        update = url_rule.get('replace')
        if update:
            a, b = update
            format_rule = re.sub(a, b, format_rule)
        new_urls, del_urls = set(), set()
        if isinstance(format_rule, basestring):
            need_format = not format_rule.startswith('http')
            for url in urls:
                # if url.startswith('http') and 'http' in format_keys:
                #     url = format_rule['http'].format(url)
                _url = None
                if meta_info and url in meta_info:
                    _url = url
                if not url.startswith('http') or need_format:
                    if '{0}' in format_rule:
                        url = format_rule.format(url)
                    # elif format_rule == True:
                    elif format_rule:
                        url = urlparse.urljoin(format_rule, url)
                        # url = urlparse.urljoin(_url, url)
                if _url:
                    meta_info[url] = meta_info.pop(_url)
                new_urls.add(url)

        elif inspect.isfunction(format_rule):
            for url in urls:
                _url = None
                if meta_info and url in meta_info:
                    _url = url
                url = format_rule(url)
                if url:
                    new_urls.add(url)
                    if _url:
                        meta_info[url] = meta_info.pop(_url)
        #         else:
        #             del_urls.add(url)

        # if len(del_urls):
        #     self.log(u'deleted {0} urls'.format(len(del_urls)))
        # else:
        #     self.log(u'没有 url 被格式化删除')
        return new_urls

    def save_request(self, requests, url_category):
        session = self.Session()
        request_model = RequestModel()
        for request in requests:
            request_model = RequestModel()
            request_model.url = request.url
            request_model.domain = self.domain
            request_model.category = url_category
            request_model.method = request.method
            request_model.headers = pickle.dumps(request.headers)
            request_model.body = pickle.dumps(request.body)
            request_model.cookies = pickle.dumps(request.cookies)
            request_model.meta = pickle.dumps(request.meta)
            request_model.encoding = request.encoding
            session.add(request_model)
        if requests:
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
            except Exception as e:
                self.log(u'Save request failed: {0}'.format(e), log.WARNING)
                session.rollback()
            else:
                self.log(u'Save request {0}'.format(request_model.url), log.INFO)
        session.close()
