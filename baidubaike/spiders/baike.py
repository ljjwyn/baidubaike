# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy_splash import SplashRequest
from baidubaike.items import BaidubaikeItem
from ..test_mongodb import get_keywords
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule,CrawlSpider


class BaikeSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        super(BaikeSpider, self).__init__(*args, **kwargs)  # 这里是关键
        self.url_set = list()

    name = 'baike'
    allowed_domains = ['www.baike.com',
                       'baike.so.com']
    # keysList = get_keywords()
    count=0
    # start_urls=[]
    # for keys in keysList:
    #     start_urls.append("http://so.baike.com/doc/" + keys)
    start_urls = ['https://baike.so.com/search/?q=神经网络']
    '''rules = {
        Rule(LinkExtractor(restrict_css='.clearfix li h4 a', tags='a', attrs='href'), follow=True, callback="parse1")
    }'''

    def parse(self, response):
        url=response.css('.res-list h3 a::attr(href)').extract_first()
        print(url)
        '''self.url_set.append(url)
        urlList = self.url_set.copy()
        print(urlList)
        print("_________________________count_________________________", len(urlList))
        for urls in urlList:
            if urls in self.url_set:
                self.url_set.remove(urls)'''
        if url:
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse2(self, response):
        print('==========================动态解析url=========================')
        item = BaidubaikeItem()
        item['ID']=self.count
        item['title'] = response.css('.content-h1 h1::text').extract_first()
        item['summary'] = response.css('.summary p::text').extract()
        item['imgUrl'] = response.xpath('//div[@class="doc-img"]//a/img/@src').extract_first()
        item['catalog'] = response.xpath('//div[@class="module zoom"]//strong').re('>(.*?)<')
        #item['content'] = response.xpath('//div[@class="module zoom"]//span').re('>(.*?)<')
        content = response.xpath('//div[@class="module zoom"]//span').extract()
        res = []
        if content:
            for c in content:
                print(c)
                contexts = ''
                a = re.compile('>(.*?)<')
                a = a.findall(c)
                while '' in a:
                    a.remove('')
                for key in a:
                    contexts += key
                res.append(contexts)
            item['content'] = res
        self.count+=1
        yield item
