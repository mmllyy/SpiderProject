# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 爬取数据的结构（糗百的首页数据结构）
class QiubaiItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img = scrapy.Field()
    content = scrapy.Field()

