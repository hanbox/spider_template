# -*- coding: utf-8 -*-
import scrapy
import logging

class MySpider(scrapy.Spider):
    name = "tmp_main"
    start_urls = []
    loop_rules = []
    extract_rules = {}

    def start_requests(self):
        urls = []
        for starturl in self.start_urls:
            urls.append(starturl['url'])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.extract_rules['list_rule']['type'] == 'css':      
            for joke in response.css(self.extract_rules['list_rule']['rule']):
                data_dict= {}
                for data in self.extract_rules['item_rules']: 
                    if data['rule']['type'] == 'css':  
                        data_dict[data['field']] = joke.css(data['rule']['rule']).extract_first().strip()
                yield data_dict             

        # next_page = response.css('div.page div a.on::attr(href)').extract()
        # if len(next_page) > 1:
        #     next_page = next_page[1]
        # else:
        #     next_page = next_page[0]
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)start_urls