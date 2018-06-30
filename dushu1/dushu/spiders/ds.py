# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from dushu.items import DushuItem

class DsSpider(CrawlSpider):
    name = 'ds'
    allowed_domains = ['www.dushu.com', 'img.dushu.com']
    start_urls = ['https://www.dushu.com/']

    # 通过连接提取器，engine自动将所有的连接加入到下载队列中
    # follow 为True时，当下载器下载的连接时，
    #        会自动提取本页的所有符合规则的连接，并加入下载队列中
    # 当连接请求成功后，由callback指定的解析函数来处理
    rules = (
        Rule(LinkExtractor(allow=r'/book/\d+_?\d*?.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/book/\d+?/'), callback='parse_book', follow=False),
    )

    def parse_item(self, response):
        i = DushuItem()  # 字典类型
        print('-----获取图书概要信息-----')
        print(response.url)
        print(response.xpath('//title/text()').extract_first())

        # 从当前的网页中获取图书信息
        books = response.xpath('//div[@class="book-info"]')
        for book in books:
            i['name'] = book.xpath('./h3/a/text()').extract_first()  # 提取第一个结果
            i['book_url'] = book.xpath('./h3/a/@href').extract_first()

            i['author'] = book.xpath('./p/a/text()').extract_first()
            i['summary'] = book.xpath('./p[last()-1]/text()').extract_first()
            i['img'] = book.xpath('.//a/img/@data-original').extract_first()

            print('----发起{}图片下载-----'.format(i['img']))
            # meta 可以实再spider之间的数据传送
            # 主要实现request和response之间的数据共享
            # meta传参时，不要使用对象的引用，需要使用常量值
            yield scrapy.Request(url=i['img'],
                                 meta={'name': i['name']},
                                 callback=self.parse_img)
            yield i

    def parse_img(self, response):
        print('-----saveImage--------')
        # response.meta 是读取request中的meta数据
        name = response.meta['name']
        print(name)
        print(response.url)

        # images 目录，是相对于dushu项目的目录
        # （参考发起命令的目录：scrapy crawl ds）
        fileName = 'images/' + name + "." + response.url.split(".")[-1]
        with open(fileName, 'wb') as f:
            f.write(response.body)


    def parse_book(self, response):
        print('-------查看图书详情---------')
        print(response.url)