# -*- coding: utf-8 -*-
import json
import codecs
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class SpiderTemplatePipeline(object):
#     def process_item(self, item, spider):
#         return item

class SpiderTemplatePipeline_JSON(object):
    def __init__(self):
        self.ids_seen = set()

    def open_spider(self, spider):
        self.file = codecs.open('tmp.json', mode='wb', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['title'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'])
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.decode("unicode_escape"))
            return item