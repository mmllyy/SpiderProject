# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

#    ????????   git 和  GitHub
from gsw import ydm_http
from scrapy.http import HtmlResponse


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
        # yield scrapy.FormRequest(url='https://so.gushiwen.org/user/login.aspx', formdata={
        yield scrapy.Request(url='https://so.gushiwen.org/RandCode.ashx', callback=self.parse)

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

    def parse(self, response: HtmlResponse):
        with open('yanzhengma.gif', 'wb') as f:
            f.write(response.body)
        print('验证码下载成功')

        # 获取图片内容
        yzmTxt = ydm_http.ydm('yanzhengma.gif')
        print(yzmTxt)

        login_url = 'https://so.gushiwen.org/user/login.aspx?'
        data = {
            'email': '610039018@qq.com',
            'pwd': 'disen8888',
            'code': yzmTxt  # 验证码数据
        }
        # post提交数据
        yield scrapy.FormRequest(url=login_url, formdata=data, callback=self.parse_zw)

    def parse_zw(self, response: HtmlResponse):
        print(response.xpath('//title/text()').extract_first())


