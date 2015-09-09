# -*- coding: utf-8 -*-
"""
数据清理过程

清理任务接口定义：

对于 UserCarItem，继承于 GpjspiderItem，清理任务名为： 去掉 Item，全小写，即 usercar

任务名则为： clean_usercar.

任务的装饰器为：
@app.task(name="clean_usedcar", bind=True, base=GPJSpiderTask)

name - 和任务名一致
bind - 为了使用配置信息和GPJSpiderTask的东西，必须为 True
base - 绑定类必须为 GPJSpiderTask

参数说明：
self - 因为绑定了类，第一个参数必须是 self
items - 要处理的 items list
args - 其他需要的参数
kwargs - 其他需要的参数

示例：

@app.task(name="clean_usedcar", bind=True, base=GPJSpiderTask)
def clean_usedcar(self, items, *args, **kwargs):
    pass


在此定义，调试完毕后，需要在 gpjspider.pipelines.clean.CleanPipeline中绑定，后期会把 Item
和 clean任务的对应放在scrapy配置中。

后期 Item 应该自动生成，可以在规则中定义 Item 的名称和使用的清理任务，在CleanPipeline中从 Item 中解析出来

"""
from .usedcars import (
    clean_usedcar,
    clean_history,
    save_to_car_source,
)