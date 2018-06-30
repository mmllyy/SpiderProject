# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import cmdline
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.linkextractors import LinkExtractor

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def __init__(self):
        super().__init__()

        # 创建selenium的chrome浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # window的chromedriver.exe文件位置
        # chrome_options.binary_location = r'd:\chromedriver.exe'

        self.brower = webdriver.Chrome(chrome_options=chrome_options)

    def parse(self, response):
        print('---parse--')
        print(response.url)

        # 通过brower打开respnse.url
        # 发起 python 关键的检索
        self.brower.get(response.url)
        self.brower.find_element_by_id('kw').send_keys('python')
        self.brower.find_element_by_id('su').click()

        time.sleep(5)
        self.brower.save_screenshot('baidu01.png')

        # 获取搜索结果,再发起请求
        links = self.brower.find_elements_by_xpath('//div[starts-with(@class,"result c-container")]/h3/a[1]')
        for link in links:

            yield scrapy.Request(link.get_attribute('href'), callback=self.parse_target)
            yield {'title': link.text,
                   'url': link.get_attribute('href')
                   }

    def parse_target(self,response):
        print('----目标网站------')
        # self.brower.get(response.url)

        return {
            'title': response.css('title::text').extract_first(),
            'url': response.url
        }



    def __del__(self):
        # 关闭brower 浏览器
        self.brower.quit()

if __name__ == '__main__':
    cmdline.execute('scrapy crawl search'.split())
