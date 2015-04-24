# -*- coding: utf-8 -*-
"""
提取 url 规则：

"""
import pickle
import inspect
from prettyprint import pp, pp_str
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
import re
import json


class GPJBaseSpider(scrapy.Spider):

    """
    公平价基本爬虫
    """

    def __init__(self, rule_path, checker_name=None, *args, **kwargs):
        """
        继承的子类必须在__init__里面调用self.checker.check()
        """
        super(GPJBaseSpider, self).__init__(*args, **kwargs)
        self.__rule_path = rule_path
        self.website_rule = {}
        self.domain = None
        self.checker_manager = CheckerManager()
        if not checker_name:
            checker_name = HIGH_QUALITY_RULE_CHECKER_NAME

        self.__checker_name = checker_name
        self.checker_class = self.checker_manager.get_checker(checker_name)
        self.checker = self.checker_class(rule_path)
        self.website_rule = self.checker.check()
        pp(self.website_rule)
        if not self.website_rule:
            raise ValueError('TODO')
        self.domain = self.website_rule['domain']

    def set_crawler(self, crawler):
        super(GPJBaseSpider, self).set_crawler(crawler)
        self.proxy_ips = self.get_proxy_ips()

    def log(self, msg, level=log.DEBUG, **kw):
        super(GPJBaseSpider, self).log(msg.encode('utf-8'), level=level, **kw)

    def get_proxy_ips(self):
        """
        """
        redis = get_redis_cluster()
        s = redis.smembers('valid_proxy_ips')
        self.log(u'all proxies: {0}'.format(s))
        if s:
            return list(s)
        else:
            return []

    def start_requests(self):
        if 'start_urls' in self.website_rule:
            start_urls = self.website_rule['start_urls']
        elif 'start_url_function' in self.website_rule:
            start_url_function = self.website_rule['start_url_function']
            start_urls = start_url_function(
                self.website_rule['start_url_template'], self
            )
        for start_url in start_urls:
            self.log(u'start request {0}'.format(start_url), log.INFO)
            yield self.make_requests_from_url(start_url)

    def parse(self, response):
        import sys
        my_name = sys._getframe().f_code.co_name
        step_rule = self.website_rule[my_name]
        if 'items' in step_rule:
            items_rule = step_rule['items']
            item_class = import_item(items_rule['class'])
            items = self.get_items(item_class, items_rule, response)
            for item in items:
                yield item
                # break
        # 提取新的 url
        if 'url' in step_rule:
            msg = u'try to get new urls from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['url'], response)
            for request in requests:
                self.log(u'start --request {0}'.format(request.url))
                yield request
                # break
        if 'next_page_url' in step_rule:
            msg = u'try to get next page url from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['next_page_url'], response)
            for request in requests:
                self.log(
                    u'start request next page: {0}.'.format(request.url))
                yield request
        if 'incr_page_url' in step_rule:
            msg = u'try to get incr page url from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['incr_page_url'], response)
            for request in requests:
                self.log(
                    u'start request next page: {0}.'.format(request.url))
                yield request

        if 'item' in step_rule:
            item_rule = step_rule['item']
            item_class = import_item(item_rule['class'])
            item = self.get_item(item_class, item_rule, response)
            yield item

    def parse_list(self, response):
        import sys
        my_name = sys._getframe().f_code.co_name
        step_rule = self.website_rule[my_name]
        if 'items' in step_rule:
            item_rule = step_rule['items']
            item_class = import_item(item_rule['class'])
            items = self.get_items(item_class, item_rule, response)
            for item in items:
                yield item
        # 提取新的 url
        if 'url' in step_rule:
            msg = u'try to get new urls from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['url'], response)
            for request in requests:
                self.log(u'start --request {0}'.format(request.url))
                yield request
        if 'next_page_url' in step_rule:
            msg = u'try to get next page url from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['next_page_url'], response)
            for request in requests:
                self.log(
                    u'start request next page: {0}.'.format(request.url))
                yield request

        if 'incr_page_url' in step_rule:
            msg = u'try to get incr page url from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            requests = self.get_requests(step_rule['incr_page_url'], response)
            for request in requests:
                self.log(
                    u'start request next page: {0}.'.format(request.url))
                yield request

        if 'item' in step_rule:
            item_rule = step_rule['item']
            item_class = import_item(item_rule['class'])
            item = self.get_item(item_class, item_rule, response)
            yield item

    def parse_detail(self, response):
        """
        """
        import sys
        my_name = sys._getframe().f_code.co_name
        step_rule = self.website_rule[my_name]
        if 'item' in step_rule:
            item_rule = step_rule['item']
            item_class = import_item(item_rule['class'])
            item = self.get_item(item_class, item_rule, response)
            yield item

    def get_requests(self, url_rule, response):
        """
        支持 xpath  re  css  json  function
        excluded中的将会被排除
        """
        urls = set()
        step_function = self.get_next_step(url_rule)
        if 'xpath' in url_rule:
            for rule in url_rule['xpath']:
                _urls = response.xpath(rule).extract()
                self.log(u'rule: {0}, urls: {1}'.format(rule, _urls))
                for _url in _urls:
                    urls.add(_url)
        if 're' in url_rule:
            for rule in url_rule['re']:
                _urls = response.selector.re(rule)
                for _url in _urls:
                    urls.add(_url)
        if 'css' in url_rule:
            for rule in url_rule['css']:
                _urls = response.css(rule).extract()
                for _url in _urls:
                    urls.add(_url)
        if 'json' in url_rule:
            for url in self.get_json(response.body, url_rule['json']):
                urls.add(unicode(url))
        if 'excluded' in url_rule:
            tmp_urls = set()
            for url in urls:
                for ex_url in url_rule['excluded']:
                    if ex_url in url:
                        tmp_urls.add(url)
                        break
            self.log(u'要删除的 URL:{0}'.format(tmp_urls), log.INFO)
            urls = urls - tmp_urls
        urls = self.format_urls(url_rule, urls)
        # for incr spider, 到达最大页号就停止
        if 'pagenum_function' in url_rule:
            pagenum_function = url_rule['pagenum_function']
            max_pagenum = url_rule.get('max_pagenum', 5)
            cur_page_num = pagenum_function(response.url)
            if cur_page_num >= max_pagenum:
                self.log(u'增量爬取到此结束')
                return []
        # 设置dont_filter比使用默认值优先级要高
        # 默认值是：如果 step 规则中有 item，则False；如果 step 规则中没有 item，则 True
        if 'dont_filter' in url_rule:
            dont_filter = url_rule['dont_filter']
        else:
            if 'item' in self.website_rule[step_function.__name__]:
                dont_filter = False
            else:
                dont_filter = True
        ret_requests = []
        if 'function' in url_rule:
            # url function 和 rule function 声明形式一样，但只能写在 rule 文件中
            # url function只能返回生成器
            # 比 rule function 多一个 url_rule参数，
            # 每次 yield 是一个 url dict,可以包含Request支持的参数
            func = url_rule.get('function')
            func_name = func.__name__
            self.log(u'try to get url from function {0}'.format(func_name))
            url_dicts = func(response, url_rule, self)
            for url_dict in url_dicts:
                if 'url' in url_dict:
                    url = url_dict.pop('url')
                else:
                    print 'no url get'
                    continue
                # self.log(u'cookies is {0}'.format(pp_str(cookies)))
                self.log(u'args is {0}'.format(pp_str(url_dict)))
                request = Request(
                    url, callback=step_function, priority=1, dont_filter=dont_filter, **url_dict)
                ret_requests.append(request)
        else:
            if urls:
                for url in urls:
                    request = Request(
                        url, callback=step_function, dont_filter=dont_filter
                    )
                    ret_requests.append(request)
        if 'update' in url_rule and 'category' in url_rule:
            if url_rule['update']:
                try:
                    self.save_request(ret_requests, url_rule['category'])
                except:
                    self.log(u'保存请求{0}时失败', level=log.ERROR)
        return ret_requests

    def get_items(self, item_class, items_rule, response):
        """
        根据 field 规则获取响应数据items
        优先级: arg/xpath > key/json > default
        """
        nodes = []
        if 'xpath' in items_rule:
            nodes = response.xpath(items_rule['xpath'])
            if items_rule['is_json']:
                nodes = self.load_json(nodes.extract()[0])
        elif 'json' in items_rule:
            json_str = response.body    # .encode('utf-8')
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
                    values = self.get_xpath(
                        xpath, response if xpath[0].startswith('//') else item_node)
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
                    if field_name == 'url' and 'format' in field:
                        # item[field_name] = field['format'].format(item[field_name])
                        item[field_name] = self.format_urls(
                            field, [item[field_name]])
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

    def get_item(self, item_class, item_rule, response):
        """
        根据 field 规则获取响应数据
        优先级: xpath > json > css > str > function > default
        """
        item = item_class()
        # 默认使用请求的 url 作为 item 的 url，如果不是这样，可以在 field 中设置 url 的规则
        item['url'] = response.url
        item['domain'] = self.domain
        for field_name, field in item_rule['fields'].iteritems():
            values = None
            if 'xpath' in field:
                values = self.get_xpath(field['xpath'], response)
            if not values:
                if 'json' in field:
                    values = self.get_json(response.body, field['json'])
                if not values:
                    if 'css' in field:
                        values = self.get_xpath(field['css'], response)
                    if not values:
                        if 'str' in field:
                            values = self.get_str(field['str'], response)
                        if not values:
                            if 'function' in field:
                                func_name = field['function']['name']
                                func = import_rule_function(func_name)
                                if not func:
                                    f = field['function']
                                    m = u'无法导入规则函数:{0}'.format(f)
                                    self.log(m, log.ERROR)
                                    continue
                                args = field['function'].get('args', tuple())
                                kwargs = field['function'].get('kwargs', {})
                                values = func(response, self, *args, **kwargs)
                            if not values:
                                if 'default' in field:
                                    item[field_name] = field['default']
                                else:
                                    # 连 default 都没有配置，就没有值了，说明规则不对
                                    m = u'field {0} 没有任何值'.format(field_name)
                                    self.log(m, log.ERROR)
            if values:
                item[field_name] = values
                # 执行处理器
                item = self.exec_processor(field_name, field, item)
            # required判断
            if field.get('required', False):
                if field_name not in item:
                    m = u'{0} is required: {1}'.format(
                        field_name, response.url)
                    raise DropItem(m)
        return item

    def get_xpath(self, xpath_rules, response):
        for xpath_rule in xpath_rules:
            values = response.xpath(xpath_rule).extract()
            if values:
                return values
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
        """
        """
        for css_rule in css_rules:
            values = response.css(css_rule).extract()
            if values:
                return values
        return []

    def get_str(self, str_rules, response):
        """
        """
        for str_rule in str_rules:
            assert len(str_rule) == 2, 'str guize  error'
            start_index = response.body.find(str_rule[0])
            if start_index == -1:
                continue
            start_index += len(str_rule[0])
            end_index = response.body.find(str_rule[1], start_index)
            if end_index == -1:
                continue
            return [response.body[start_index:end_index]]
        return []

    def exec_processor(self, field_name, field_rule, item):
        """
        根据字段规则定义和当前 item，对此字段进行过滤，暂时不支持 processor参数
        """
        base_processors = []
        processors = field_rule.get('processors', [])
        processors += base_processors
        for processor in processors:
            processor_func = import_processor(processor)
            if not processor_func:
                self.log(u'无此处理器:{0}'.format(processor))
                return item
            item[field_name] = processor_func(item[field_name])
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
            self.log(
                u'object {0} is instance of {1}'.format(n, cn), level=log.ERROR)
            return None
        return step

    def format_urls(self, url_rule, urls):
        """
        有些时候一个简单地格式化字符串就可以得到最终的 url，有时候需要对 url 进一步处理。
        比如: 得到的 url 是这样的：

        javascript:window.open('http://bj.haoche51.com/details/20003.html')
        这种情况下，只能去自定义函数去处理了
        """
        self.log(u'原始 URL:{0}'.format(urls))
        if 'format' not in url_rule:
            return urls
        format_rule = url_rule['format']
        new_urls, del_urls = set(), set()
        if isinstance(format_rule, basestring):
            for url in urls:
                new_urls.add(format_rule.format(url))
        elif inspect.isfunction(format_rule):
            for url in urls:
                _url = format_rule(url)
                if _url:
                    new_urls.add(_url)
                else:
                    del_urls.add(url)
        if del_urls:
            self.log(u'以下 url 被删除:{0}'.format(del_urls))
        else:
            self.log(u'没有 url 被格式化删除')
        return new_urls

    def save_request(self, requests, url_category):
        Session = get_mysql_connect()
        session = Session()
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
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
        except Exception as e:
            self.log(u'未知异常：{0}'.format(e), log.ERROR)
            session.rollback()
        else:
            self.log(u'成功保存请求{0}'.format(request_model.url), log.INFO)
