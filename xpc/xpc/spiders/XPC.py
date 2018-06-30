# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class XpcSpider(scrapy.Spider):
    name = 'XPC'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/id-0/sort-addtime/type-0']
    # redis_key = 'XPC:start_urls'


    def parse(self, response:HtmlResponse):
        print(response.status)
        with open('video.html','wb') as f:
            f.write(response.body)
        print('---'*100)
        #
        links = response.xpath('//div[@class="channel-con"]/ul/li')
        # print(links)
        for link in links:
            try:
                video_name = link.xpath('.//p[@class="fs_14 fw_600 c_b_3 line-hide-1"]/text()').extract()[0]
                print(video_name)
                image_url = link.xpath('./a[@class="video-cover"]/img/@_src').extract()[0]
                print(image_url)
                video_author = link.xpath("./div/div/a/span[@class='name fs_12 fw_300 c_b_3 v-center line-hide-1']/text()").extract()[0]
                print(video_author)
                release_date = link.xpath('./a/div/p/text()').extract()[0]
                print(release_date)
                data = link.xpath('./@data-articleid').extract()[0]
                href = 'http://www.xinpianchang.com/a'+data+'?from=ArticleList'

            except:
                pass
            else:
                print(href)
                # 发起详情页面的请求
                yield scrapy.Request(href,meta={'video_name':video_name,'image_url':image_url,
                                                'video_author':video_author,'release_date':release_date},
                                                callback=self.parse_video)
                print('----------'*30)

        next_url = response.xpath('//a[@title="下一页"]/@href').extract()[0]
        yield scrapy.Request(next_url,callback=self.parse)


    def parse_video(self,response:HtmlResponse):
        print('进来了')
        with open('video_info.html','wb') as f:
            f.write(response.body)
        video_url = response.xpath('//source/@src').extract_first()  #   ????
        yield {
            "video_name": response.meta['video_name'],
            "image_url": response.meta['image_url'],
            "video_author": response.meta['video_author'],
            "release_date": response.meta['release_date'],
            "video_url":video_url,
        }









