# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import settings
from scrapy import signals

class SpiderTemplateSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    #json of template setting
    SETTING_JSON = {}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        print '********** from_crawler ***********'
        s = cls()

        #load config
        with open('setting_template.json') as json_file:
            s.SETTING_JSON = json.load(json_file)
        # logging.debug(s.SETTING_JSON)

        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.name = self.SETTING_JSON['template_name']
        spider.start_urls = self.SETTING_JSON['start_urls']
        spider.loop_rules = self.SETTING_JSON['loop_rules']
        spider.extract_rules = self.SETTING_JSON['extract_rules']

        #other setting
        settings.CONCURRENT_REQUESTS = self.SETTING_JSON['other_setting']['concurrent_requests']
        settings.DOWNLOAD_DELAY = self.SETTING_JSON['other_setting']['download_delay']
        
        spider.logger.info('Spider opened: %s' % spider.name)