# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import cmdline
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.linkextractors import LinkExtractor

class SearchSpider(scrapy.Spider):
    name = 'search_1'
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
        # 基于连接提取器，获取查询结构连接
        extractor = LinkExtractor(r'http://www.baidu.com/link\?.*')

        print('---extractor---')
        response.text = self.brower.page_source

        # 开始提取
        links = extractor.extract_links(response)
        for link in links:
            print(link)
            # print('title:', link.text)
            # print('url:', link.url)
            # yield {
            #     'title': link.text,
            #     'url': link.url
            # }

    def __del__(self):
        # 关闭brower 浏览器
        self.brower.quit()

if __name__ == '__main__':
    cmdline.execute('scrapy crawl search'.split())
