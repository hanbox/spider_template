# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import settings
from user_agents import agents
from scrapy import signals
from scrapy.conf import settings

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class SpiderTemplateSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    #json of template setting
    SETTING_JSON = {}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
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
        spider.extract_rules = self.SETTING_JSON['extract_rules']

        #other setting
        # spider.settings['DOWNLOAD_DELAY'] = self.SETTING_JSON['other_setting']['download_delay']
        # spider.settings.set('CONCURRENT_REQUESTS',self.SETTING_JSON['other_setting']['concurrent_requests'])
        # spider.settings.set('DOWNLOAD_DELAY',int(self.SETTING_JSON['other_setting']['download_delay']))

        print '*************'
        print spider.settings['DOWNLOAD_DELAY']
        print type(spider.settings['DOWNLOAD_DELAY'])
        
        spider.logger.info('Spider opened: %s' % spider.name)