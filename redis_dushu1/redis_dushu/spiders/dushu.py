# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule


class DushuSpider(RedisCrawlSpider):
    name = 'dushu'
    allowed_domains = ['www.dushu.com']

    redis_key = 'dushu:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'/book/\d+_?\d*?.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        books = response.xpath('//div[@class="book-info"]')
        for book in books:
            i['name'] = book.xpath('./h3/a/text()').extract_first()  # 提取第一个结果
            i['book_url'] = book.xpath('./h3/a/@href').extract_first()

            i['author'] = book.xpath('./p/a/text()').extract_first()
            i['summary'] = book.xpath('./p[last()-1]/text()').extract_first()
            i['img'] = book.xpath('.//a/img/@data-original').extract_first()

        return i