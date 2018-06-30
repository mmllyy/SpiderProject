# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import cmdline
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.linkextractors import LinkExtractor

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def __init__(self):
        super().__init__()
        # 创建selenium的Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')


        self.brower = webdriver.Chrome(chrome_options=chrome_options)


    def parse(self, response:HtmlResponse):
        print('---parse---')
        print(response.url)
        # 通过
        self.brower.get(response.url)
        self.brower.find_element_by_id('kw').send_key('python')
        self.brower.find_element_by_id('su').click()
        time.sleep(5)
        # self.brower.
        self.brower.save_screenshot('baidu01.png')
        extractor = LinkExtractor(r'http://www.baidu.com/link\?.*')

        links = extractor.extract_links(self.brower)



    def __del__(self):
        self.brower.close()



if __name__ == '__main__':
    cmdline.execute('scrapy crawl search'.split())