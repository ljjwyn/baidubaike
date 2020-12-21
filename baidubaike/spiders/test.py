# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders.crawl import Rule,CrawlSpider

from baidubaike.test_mongodb import get_keywords


class BaikeSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super(BaikeSpider, self).__init__(*args, **kwargs)  # 这里是关键
        self.url_set = list()

    name = 'test'
    allowed_domains = ['www.baike.com',
                       'baike.so.com']
    keysList = get_keywords()
    count=0
    start_urls=["https://baike.so.com/search/?q=%E4%BC%A6%E6%95%A6"]
    #start_urls = ['http://so.baike.com/doc/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD']'''
    '''rules = {
        Rule(LinkExtractor(restrict_css='.clearfix li h4 a', tags='a', attrs='href'), follow=True, callback="parse1")
    }'''

    def parse1(self, response):
        url=response.css('.result-list h3 a::attr(href)').extract_first()
        '''self.url_set.append(url)
        urlList = self.url_set.copy()
        print(urlList)
        print("_________________________count_________________________", len(urlList))
        for urls in urlList:
            if urls in self.url_set:
                self.url_set.remove(urls)'''
        if url:
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse(self, response):

        content=response.css('.res-list h3 a::attr(href)').extract()
        print(content)
        res=[]
        for c in content:
            print(c)
            contexts=''
            a=re.compile('>(.*?)<')
            a=a.findall(c)
            while '' in a:
                a.remove('')
            for key in a:
                contexts+=key
            res.append(contexts)
        print(res)

