# -*- coding: utf-8 -*-

from gpjspider.tasks.clean import clean_usedcar


class CleanPipeline(object):

    """
    调用 clean task.每次先缓存10个之后才调用
    """

    def __init__(self, settings):
        if not settings.getint('CLEAN_ITEM_CACHE_NUM'):
            self.clean_item_cache_num = 10
        self.clean_item_cache_num = settings.getint('CLEAN_ITEM_CACHE_NUM')
        # 暂时只支持 UsedCarItem， todo， 或者从 gpjspider.item中自行读取
        # 注册 item 和对应的清理任务
        self.cached_item = {
            'UsedCarItem': []
        }
        self.clean_tasks = {
            'UsedCarItem': clean_usedcar
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        cls = item.__class__.__name__
        caches = self.cached_item[cls]
        caches.append(item)
        num = len(caches)
        if num >= self.clean_item_cache_num:
            clean_task = self.clean_tasks[cls]
            items = caches[:num]
            self.cached_item[cls] = caches[num:]
            spider.log(u'clean_task: {0}'.format(clean_task.name))
            # clean_task.delay(items)
            clean_task(items)

    def close_spider(self, spider):
        for class_name, items in self.cached_item.iteritems():
            clean_task = self.clean_tasks[class_name]
            spider.log(u'清理 {0} 的最后{1}个数据。'.format(class_name, len(items)))
            # clean_task.delay(items)
            clean_task(items)
        # spider.log(u'清理结束，爬虫退出')
