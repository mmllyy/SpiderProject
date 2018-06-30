# -*- coding: utf-8 -*-
import scrapy
from redis_dushu.items import RedisDushuItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule


class DsSpider(RedisCrawlSpider):
    name = 'ds'
    # allowed_domains = ['www.dushu.com']
    # start_urls = ['http://www.dushu.com/']
    allowed_domains = ['www.dushu.com']

    redis_key = 'dushu:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'/book/\d+_?\d*?.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        print('--------获取图书概要信息----------')
        print(response.url)
        print(response.xpath('//title/text()').extract()[0])
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()

        # 从当前的网页中获取图书信息
        books = response.xpath('//div[@class="book-info"]')
        for book in books:
            i['name'] = book.xpath('./h3/a/text()').extract_first()
            i['book_url'] = book.xpath('./h3/a/@href').extract_first()
            i['author'] = book.xpath('./p/a/text()').extract_first()
            i['summary'] = book.xpath('./p[last()-1]/text()').extract_first()
            i['img'] = book.xpath('.//a/img/@data-original').extract_first()
            print('----发起{}图片下载-----'.format(i['img']))
            # meta 可以实再spider之间的数据传送
            # 主要实现request和response之间的数据共享
            # meta传参时，不要使用对象的引用，需要使用常量值
            # yield scrapy.Request(url=i['img'],
            #                      meta={'name': i['name']},
            #                      callback=self.parse_img)

            yield i
