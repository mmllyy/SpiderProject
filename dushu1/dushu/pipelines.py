# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import requests

from dushu import settings


class DushuPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='root',
                                  db='ds',
                                  charset='utf8')
        self.cursor = self.db.cursor()


    def close_spider(self,spider):
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        # 向数据库写入
        print('----item写入数据库的Pipeline------')
        print(item['name'])
        sql = 'select id from book where name=%s'
        self.cursor.execute(sql, args=(item['name'],))
        print('查询结果：', self.cursor.rowcount)
        if self.cursor.rowcount ==0:
            sql = 'insert book(name,author,img,summary,book_url) values(%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,args=(
                item['name'],
                item['author'],
                item['img'],
                item['summary'],
                item['book_url']
            ))

            if self.cursor.rowcount >=1:
                print(item['name'], '写入成功')

        return item


class ImagePipeline(object):

    def process_item(self, item, spider):

        # 下载图片
        print('----item保存图片的Pipeline------')

        fileName = 'images/'+item['name']+"."+item['img'].split(".")[-1]
        with open(fileName, 'wb') as f:
            f.write(item['img_body'])

        del item['img_body']


