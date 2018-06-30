
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import json

import scrapy


class FanyiSpider(scrapy.Spider):
    name = 'fy'
    allowed_domain = ['fanyi.baidu.com']
    #  http://fanyi.baidu.com/
    # start_urls = ['http://fanyi.baidu.com']
    def parse(self,response):
        print('ok',response.url)
        print(response.body)
        jsonObj = json.loads(response.body,encoding='utf-8')
        print(jsonObj)

    def start_requests(self):
        print('开始')
        # yield scrapy.Request(url='http://fanyi.baidu.com',callback=self.parse)
        url = 'http://fanyi.baidu.com/sug'
        data = {
            'kw':'李世民'
        }
        yield scrapy.FormRequest(url=url,formdata=data,callback=self.parse)
        yield scrapy.FormRequest(url='http://fanyi.baidu.com/v2transapi',formdata={

        })