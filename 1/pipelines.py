# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class QiubaiPipeline(object):

    # 开始打开spider时，回调的函数
    def open_spider(self, spider):
        print('---open_spider----')
        # 连接数据库
        self.db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='qb',
            charset='utf8'
        )
        # 打开数据库操作对象（游标）
        self.cursor = self.db.cursor()
        print('---连接库连接成功---')

    # 完成spdier时， 回调的函数
    def close_spider(self, spider):
        print('---close_spider----')
        self.db.close()  # 关闭数据库连接

    # item 管道在接收 spider的parse返回的item时
    # 由当前的item管道process_item()处理
    def process_item(self, item, spider):
        print('---process item---')
        # print(item['name'], item['img'])

        # 将数据库写入到数据库中
        self.cursor.execute('insert content(name,img,content) values(%s,%s,%s)',
                            args=(item['name'],
                                  item['img'],
                                  item['content']))
        self.db.commit()  # 提交事务
        if self.cursor.rowcount >=1:
            print(item['name'], '数据写入成功！')

        return item
