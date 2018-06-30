# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class QiubaiPipeline(object):
    def open_spider(self,spider):
        print('--************-open_spider-***************--')
        # 连接数据库
        self.db = pymysql.connect(
            host="10.35.163.12",
            port=3306,
            user="root",
            password="root",
            db="qb",
            charset="utf8"
        )
        self.cursor = self.db.cursor()
        print('---数据库连接成功')


    def close_spider(self, spider):
        print('---close_spider---')
        self.db.close()  # 关闭数据库连接


    def process_item(self, item, spider):
        print('---process item---')
        print(item['name'],item['img'])
        # 将数据写入到数据库中
        self.cursor.execute('insert content(name,img,content) values(%s,%s,%s)',
                            args=(item['name'],item['img'],item['content']))
        self.db.commit()
        if self.cursor.rowcount >=1:
            print(item['name'],'数据写入成功')
        return item
