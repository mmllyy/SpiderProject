# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import cmdline
from scrapy.http import HtmlResponse
# from selenium.webdriver.chrome import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from scrapy.linkextractors import LinkExtractor


class SearchSpider(scrapy.Spider):
    name = 'search1'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def __init__(self):
        super().__init__()
        # 创建selenium的Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.binary_location = r'd:\chromedriver.exe'

        self.brower = webdriver.Chrome(executable_path=r'e:\chromedriver.exe',
                                        chrome_options=chrome_options)

    def parse(self, response: HtmlResponse):
        print('---parse---')
        print(response.url)
        # 通过
        self.brower.get(response.url)
        self.brower.find_element_by_id('kw').send_keys('python')
        self.brower.find_element_by_id('su').click()
        time.sleep(5)
        # self.brower.
        self.brower.save_screenshot('baidu01.png')
        # extractor = LinkExtractor(r'http://www.baidu.com/link\?.*')

        #    ???????
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
    cmdline.execute('scrapy crawl search1'.split())
