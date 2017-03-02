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

class myImagesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):  
        image_guid = request.url.split('/')[-1]  
        return 'spider_funpic/file/full/%s' % (image_guid)  

    def get_media_requests(self, item, info):   
        if item['data_type'] == 'funpics':
            for image_url in item['image_paths']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        if item['data_type'] == 'jokes':
            return item   
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths[0]
        return item