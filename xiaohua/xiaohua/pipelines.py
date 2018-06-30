# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from xiaohua import settings


class DBPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #  下载图片
        for image in item['imgs']:
            yield scrapy.Request(url=image, meta={
                'name': item['name']
            })

    def file_path(self, request, response=None, info=None):
        #  返回存储的文件名
        dirPath = os.path.join(settings.IMAGES_STORE, request.meta['name'])
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)

        return request.meta['name']+"/"+request.url.split('/')[-1]
