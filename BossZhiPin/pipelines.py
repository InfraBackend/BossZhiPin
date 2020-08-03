# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time


class BossZhiPinPipeline(object):
    def process_item(self, item, spider):
        return item


class ImportToJson(object):
    # 创建json文件
    def __init__(self):
        # 构建json文件的名称
        jsonName = 'bosszhipin_' + str(time.strftime("%Y%m%d", time.localtime())) + '.json'
        self.f = open(jsonName, 'w')

    # 打开爬虫时
    def open_spider(self, spider):
        pass

    # 主管道
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content)
        return item

    # 爬虫关闭时
    def close_spider(self, spider):
        self.f.close()
