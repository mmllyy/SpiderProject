# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class DySpider(scrapy.Spider):
    name = 'dy'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/index.html']

    def parse(self, response:HtmlResponse):
        print(response.status)
        with open('movie.html','wb') as f:
            f.write(response.body)
        print('---'*100)
        links = response.xpath('//div[@class="co_area2"]/div[@class="co_content8"]/ul//table[@class="tbspan"]/tr[2]/td[2]//a')
        #print(links)
        for link in links:
            try:
                name = link.xpath('./text()').extract()[0]
                href = link.xpath('./@href').extract()[0]
                href = 'http://www.dytt8.net'+href
            except:
                pass
            else:
                print(name,href)
                # 发起详情页面的请求
                yield scrapy.Request(href,callback=self.parse_video)
                print('----------'*30)

    def parse_video(self,response:HtmlResponse):
        print('进来了')
        with open('movie_info.html','w') as f:
            f.write(response.text)
        # 解析详细的电影页面
        title = response.xpath('//h1/font/text()').extract()[0]
        # //ul/div[@id='Zoom']/span/table[1]/tbody/tr/td/a
        video_url = response.xpath('//table/tbody//a/@href').extract()[0]  #   ????
        print('---准备下载---',video_url)
        # yield scrapy.Request(video_url,callback=self.saveVideo)
    #
    # def saveVideo(self,response):
    #     print('---保存视频---')
    #     print('url:',response.url)





