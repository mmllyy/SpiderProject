# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

class GuShiWenSpider(scrapy.Spider):
    name = 'gsw'

    allowed_domain = ['www.gushiwen.org', 'so.gushiwen.org', 'www.ip138.com']

    def start_requests(self):
        # 开始发出请求任务
        print('---GSW 开始发起请求----')

        yield scrapy.Request(url='https://so.gushiwen.org/mingju/',
                             callback=self.parse_mg)

        yield scrapy.Request(url='https://www.gushiwen.org/shiwen/',
                              callback=self.parse_sw)

        yield scrapy.Request(url='http://www.ip138.com/',
                             callback=self.parse_ip)


    def parse_mg(self, response):
        print('----开始解析名句-----')
        print(response.xpath('//title/text()').extract_first())


    def parse_sw(self, response):
        print('---开始解析诗文----')
        print(response.xpath('//title/text()').extract_first())

    def parse_ip(self, response):
        print('---本地ip查询----')
        with open('ip.html', 'wb') as f:
            f.write(response.body)