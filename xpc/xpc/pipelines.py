# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from xpc import settings


class XpcPipeline(object):
    def open_spider(self,spider):
        print('--************-open_spider-***************--')
        self.db = pymysql.connect(
            host="10.35.163.12",
            port=3306,
            user="root",
            password="root",
            db="xpc",
            charset="utf8"
        )
        self.cursor = self.db.cursor()
        print('---数据库连接成功')


    def close_spider(self, spider):
        print('---close_spider---')
        self.db.close()

    def process_item(self, item, spider):
        print('---process item---')
        # 将数据写入到数据库中
        self.cursor.execute('insert video(video_name,image_url,video_author,release_date,video_url) '
                            'values(%s,%s,%s,%s,%s)',
                            args=(item['video_name'],item['image_url'],item['video_author'],
                                  item['release_date'],item['video_url']))
        self.db.commit()
        if self.cursor.rowcount >=1:
            print(item['video_name'],'数据写入成功')
        return item



class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #  下载图片

        yield scrapy.Request(url=item['image_url'], meta={'name': item['video_name'] })

    def file_path(self, request, response=None, info=None):
        #  返回存储的文件名
        # dirPath = os.path.join(settings.IMAGES_STORE, request.meta['name'])
        # if not os.path.exists(dirPath):
        #     os.mkdir(dirPath)

        return request.meta['name']+"."+request.url.split('.')[-1]
