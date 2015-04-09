# -*- coding: utf-8 -*-
"""
提取 url 规则：

"""
import inspect
from rediscluster import RedisCluster
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem
from gpjspider.utils.path import import_rule_function, import_item
from gpjspider.utils.path import import_processor
from gpjspider.checkers import CheckerManager


class GPJBaseSpider(scrapy.Spider):
    """
    公平价基本爬虫
    """

    def __init__(self, rule_path, *args, **kwargs):
        """
        继承的子类必须在__init__里面调用self.checker.check()
        """
        super(GPJBaseSpider, self).__init__(*args, **kwargs)
        self.__rule_path = rule_path
        self.website_rule = {}
        self.domain = None
        self.checker_manager = CheckerManager()

    def set_crawler(self, crawler):
        super(GPJBaseSpider, self).set_crawler(crawler)
        self.redis_config = crawler.settings.getlist('REDIS_CONFIG')
        self.proxy_ips = self.get_proxy_ips()

    def log(self, msg, level=log.DEBUG, **kw):
        """
        因为是通用爬虫，message 带上域名，以便识别
        """
        msg = u"{0}: {1}".format(self.domain, msg)
        super(GPJBaseSpider, self).log(msg.encode('utf-8'), level=level, **kw)

    def get_proxy_ips(self):
        """
        """
        redis = RedisCluster(startup_nodes=self.redis_config)
        s = redis.smembers('valid_proxy_ips')
        self.log(u'代理是 {0}'.format(s))
        if s:
            return list(s)
        else:
            return []

    def start_requests(self):
        """
        """
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
        # 提取新的 url
        if 'url' in step_rule:
            msg = u'try to get new urls from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            urls = self.get_urls(step_rule['url'], response)
            step_function = self.get_next_step(step_rule, 'url')
            urls = self.format_urls(step_rule['url'], urls)
            for url in urls:
                self.log(u'start --request {0}'.format(url), level=log.DEBUG)
                yield Request(url, callback=step_function)
        if 'next_page_url' in step_rule:
            msg = u'try to get next page url from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            urls = self.get_urls(step_rule['next_page_url'], response)
            step_function = self.get_next_step(step_rule, 'next_page_url')
            urls = self.format_urls(step_rule['next_page_url'], urls)
            for url in urls:
                self.log(u'start request next page: {0}.'.format(url))
                yield Request(url, callback=step_function)

        if 'item' in step_rule:
            item_rule = step_rule['item']
            item_class = import_item(item_rule['class'])
            item = self.get_item(item_class, item_rule, response)
            yield item

    def parse_list(self, response):
        import sys
        my_name = sys._getframe().f_code.co_name
        step_rule = self.website_rule[my_name]
        # 提取新的 url
        if 'url' in step_rule:
            msg = u'try to get new urls from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            urls = self.get_urls(step_rule['url'], response)
            step_function = self.get_next_step(step_rule, 'url')
            urls = self.format_urls(step_rule['url'], urls)
            for url in urls:
                self.log(u'start --request {0}'.format(url), level=log.DEBUG)
                yield Request(url, callback=step_function)
        if 'next_page_url' in step_rule:
            msg = u'try to get next page url from {0}'.format(response.url)
            self.log(msg, level=log.DEBUG)
            urls = self.get_urls(step_rule['next_page_url'], response)
            step_function = self.get_next_step(step_rule, 'next_page_url')
            urls = self.format_urls(step_rule['next_page_url'], urls)
            for url in urls:
                self.log(u'start request next page {0}'.format(url))
                yield Request(url, callback=step_function)

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

    def get_urls(self, url_rule, response):
        """
        支持 xpath re css  json
        excluded中的将会被排除
        """
        urls = set()
        if 'xpath' in url_rule:
            for rule in url_rule['xpath']:
                _urls = response.xpath(rule).extract()
                for _url in _urls:
                    urls.add(_url)
        if 're' in url_rule:
            for rule in url_rule['re']:
                _urls = response.re(rule)
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
            urls = urls - tmp_urls
        return urls

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
                    m = u'{0} is required:{1}'.format(field_name, response.url)
                    raise DropItem(m)
        return item

    def get_xpath(self, xpath_rules, response):
        """
        """
        try:
            for xpath_rule in xpath_rules:
                values = response.xpath(xpath_rule).extract()
                if values:
                    return values
        except:
            self.log('test_____:{0}'.format(xpath_rules), level=log.ERROR)
        return []

    def get_json(self, json_unicode, json_path):
        """
        处理一段 json 字符串
        """
        import json
        try:
            jso = json.loads(json_unicode)
        except Exception as e:
            self.log(str(e), level=log.ERROR)
            return None
        else:
            return self.parse_json_path(json_path, jso)

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

    def get_next_step(self, current_step_rule, url_name):
        """
        仅当step_rule有 url 或者 next_page_url 规则时可用
        """
        step_name = current_step_rule[url_name]['step']
        step = getattr(self, step_name)
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
