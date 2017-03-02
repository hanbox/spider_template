# -*- coding: utf-8 -*-
import scrapy
import logging
from spider_template.items import SpiderTemplateItem

class MySpider(scrapy.Spider):
    name = "tmp_main"
    start_urls = []
    extract_rules = {}

    data_dict = {}

    def start_requests(self):
        urls = []
        for starturl in self.start_urls:
            urls.append(starturl['url'])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        print '**********************'
        scrapy.statscol.StatsCollecto.get_stats()

    def parse(self, response):
        return self.parse_detail(response, self.extract_rules)

    def parse_child(self, response):
        child_ectract = response.meta['child_ectract']
        response.meta['child_ectract'] = {}
        return self.parse_detail(response, child_ectract)

    def parse_detail(self, response, detail_rules):
        try:
            if detail_rules['list_rule']:
                if detail_rules['list_rule']['type'] == 'css':      
                    for data_detail in response.css(detail_rules['list_rule']['rule']):
                        yield self.getdict(data_detail, detail_rules)       
            elif detail_rules['item_rules']:
                yield self.getdict(response, detail_rules)

            if detail_rules['loop_rules']:
                for data in detail_rules['loop_rules']: 
                    next_page= []
                    if data['type'] == 'css':  
                        next_page = response.css(data['rule']).extract()
                    elif data['type'] == 'xpath':  
                        next_page = response.xpath(data['rule']).extract()
                    elif data['type'] == 'reg':  
                        next_page = response.reg(data['rule']).extract()

                    if next_page:
                        if len(next_page) > 1:
                            next_page = next_page[1]
                        else:
                            next_page = next_page[0]
                        next_page = response.urljoin(next_page)
                        # yield scrapy.Request(next_page, callback=self.parse)
        except Exception, e:
            pass

    def getdict(self, response, detail_rules):
        self.data_dict = {}
        for data in detail_rules['item_rules']: 
            #content
            data_extract = ""

            try:
                if data['rule']['type'] == 'css':  
                    data_extract = response.css(data['rule']['rule']).extract_first()
                elif data['rule']['type'] == 'xpath':  
                    data_extract = response.xpath(data['rule']['rule']).extract_first()
                elif data['rule']['type'] == 'reg':  
                    data_extract = response.reg(data['rule']['rule']).extract_first()

                if data['rule']['isTrim'] is True:
                    self.data_dict[data['field']] = data_extract.strip()
                else:
                    self.data_dict[data['field']] = data_extract

            except Exception, e:
                pass

            #url
            try:
                url_extract = ""
                if len(data['url_rule']['type']) and len(data['url_rule']['rule']):
                    if data['url_rule']['type'] == 'css':  
                        url_extract = response.css(data['url_rule']['rule']).extract_first()
                    elif data['url_rule']['type'] == 'xpath':  
                        url_extract = response.xpath(data['url_rule']['rule']).extract_first()
                    elif data['url_rule']['type'] == 'reg':  
                        url_extract = response.reg(data['url_rule']['rule']).extract_first()
                    if url_extract:
                        url_extract = url_extract.strip()
                        self.data_dict['url' + '_' + data['field']] = url_extract
                        if data['url_rule']['isRec'] is True: 
                            pass
                        # return scrapy.Request(url=url_extract, callback=self.parse_child, meta={'child_ectract': data['depth_rule']})
            except Exception, e:
                pass

        return self.data_dict