# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class QbSpider(scrapy.Spider):
    # Spider名字  ，在命令行中，使用crawl命令，并指定qb的name名，开始爬数据
    name = 'qb'

    # 在请求站点资源时，资源只能是指定的域名下的资源
    allowed_domains = ['www.qiushibaike.com']

    # 爬虫开始爬取资源的入口
    start_urls = ['https://www.qiushibaike.com/']

    # 当请求的资源成功时，回调parse函数，
    # 进行数据解析
    # parser如果有返回数据，则返回可迭代对象（列表，元组，字符串）
    def parse(self, response:HtmlResponse):
        # print('---'*100)
        # response是响应对象，常用属性
        # print(response.encoding)   # 不能修改
        # print(response.headers)
        # print(response.status)
        # print(response.url)
        # print(response.request.url)

        # 直接查询网页中的title标签，
        # print(response.xpath('//title/text()'))
        # print(response.text)  # 打印文本数据
        # print(response.body)
        # print(response.selector.xpath('//div[starts-with(@class,"author")]/a'))
        # print(response.css('div[class="author clearfix"] a'))
        # from qiubai.qiubai.items import QiubaiItem

        articles = response.xpath('//div[starts-with(@class,"article")]')
        for article in articles:
            try:
                name = article.xpath('./div[1]//img/@alt').extract()[0]
                img = article.xpath('./div[1]//img/@src').extract()[0]
                content = article.xpath('.//div[@class="content"]/span[1]/text()').extract()
            except:
                pass
            else:
                # print(name,img)
                # print(''.join(content).replace('\n',''))
                # item = QiubaiItem()
                # item.name = name
                # item.img = 'http:'+img
                # item.content = ''.join(content).replace('\n','')
                # 将item
                yield {
                    "name":name,
                    "img":'http:'+img,
                    'content':''.join(content).replace('\n','')
                }

        # print('---'*100)

# //div[starts-with(@class,"article")]/div[1]//img/@src
# //div[starts-with(@class,"article")]//div[@class="content"]
# //div[starts-with(@class,"article")]//div[@class="thumb"]//img/@src

        # 读取下一页数据
        next_url = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').extract()[0]
        next_page_url = response.urljoin(next_url)
        print(next_page_url)
        yield scrapy.Request(next_page_url,callback=self.parse)
        # print(next_url)
        print('---'*100)