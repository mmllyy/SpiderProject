# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DushuItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 书名
    img = scrapy.Field()  # 图片地址
    img_body = scrapy.Field()
    author = scrapy.Field()  # 作者
    summary = scrapy.Field()  # 概要说明

    book_url = scrapy.Field()  # 书的详细地址
