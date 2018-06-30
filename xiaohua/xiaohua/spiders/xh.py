# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class XhSpider(RedisCrawlSpider):
    name = 'xh'
    allowed_domains = ['www.meinv.hk']
    # start_urls = ['http://www.521609.com/']
    # 设置Redis存储爬虫起始的入口url的key
    redis_key = 'xh:start_urls'

    rules = (
        Rule(LinkExtractor(r'http://www.meinv.hk/.p=\d{4}'), callback='parse_item', follow=True),
    )

    def parse_item(self, response:HtmlResponse):
        print('----------------获取的url------------------')
        print(response.url)

        i = {'name':response.css('h1[class="title"]::text').extract_first(),
             'imgs':response.css('div[class="post-image"] img::attr(src)').extract(),
             'url':response.url}
        return i

if __name__ == '__main__':
    cmdline.execute('scrapy runspider xh.py'.split())

