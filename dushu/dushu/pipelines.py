# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib

import pymysql


class DushuPipeline(object):
    def open_spider(self,spider):
        print('--************-open_spider-***************--')
        # 连接数据库
        self.db = pymysql.connect(
            host="10.35.163.12",
            port=3306,
            user="root",
            password="root",
            db="ds",
            charset="utf8"
        )
        self.cursor = self.db.cursor()
        print('---数据库连接成功')


    def close_spider(self, spider):
        print('---close_spider---')
        self.db.commit()
        self.db.close()  # 关闭数据库连接


    def process_item(self, item, spider):
        # 向数据库写入
        print('---写数据库---')
        sql = 'select id from shu where name=%s'
        self.cursor.execute(sql,args=(item['name']))
        if self.cursor.rowcount ==0:
            sql = 'insert shu(name,img,summary,book_url,author) values(%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,
                            args=(item['name'], item['img'], item['summary'], item['book_url'], item['author']))
            if self.cursor.rowcount >= 1:
                print(item['name'], '数据写入成功')
        return item


class ImgPipeline(object):
    def process_item(self, item, spider):
        # 向数据库写入
        # print('---保存图片---')
        # fileName = './imgs'+item['name']+'.'+item['img'].split('.')[-1]
        # urllib.request.urlretrieve(item['img'],fileName)
        # print('下载图片成功')

        return item
