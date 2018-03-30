# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy项目.demo.demo import settings
pymysql.install_as_MySQLdb()


class DemoPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()  # 获取一个游标

    def process_item(self, item, spider):
        try:
            novel_name = item['novel_name']
            book_name = item['book_name']
            book_url = item['book_url']
            book_context = item['book_context']
            self.do_insert(novel_name, book_name, book_url, book_context)
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item

    def do_insert(self, novel_name, book_name, book_url, book_context):
        sql = "insert into demo_novel(novel_name, book_name, book_url, book_context)" \
              " values('%s', '%s', '%s', '%s')" % (novel_name, book_name, book_url, book_context)
        self.cursor.execute(sql)
        self.connect.commit()

    def close_session(self, item):
        self.cursor.close()  # 关闭游标
        self.connect.close()  # 释放数据库资源

    # def __init__(self):
    #     self.file = open('qswbook.json', 'w', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     result = json.dumps(dict(item), ensure_ascii=False) + ";\n"
    #     self.file.write(result)
    #     return item
    #
    # def close_spider(self):
    #     self.file.close()

    # 数据存入本地
    # def process_item(self, item, spider):
    #     with open('qswbook.txt', 'a', encoding='utf-8') as f:
    #         book_names = item['book_name']
    #         book_urls = item['book_url']
    #         for i, j in zip(book_names, book_urls):
    #             f.write(i + ':' + j + '\n')
    #         f.close()
    #     return item
    # def process_item(self, item, spider):
    #

    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbparms = dict(
    #         host=settings["MYSQL_HOST"],
    #         db=settings["MYSQL_DBNAME"],
    #         user=settings["MYSQL_USER"],
    #         passwd=settings["MYSQL_PASSWORD"],
    #         charset="utf8",
    #         cursorclass=pymysql.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
    #     return cls(dbpool)
    #
    # def process_item(self, item, spider):
    #     # 使用twisted将mysql插入编程一部执行
    #     query = self.dbpool.runInteraction(self.do_insert, item)
    #     query.addErrback(self.handle_error, item, spider)
    #
    # def handle_error(self, failure, item, spider):
    #     # 处理异步插入的异常
    #     print(failure)
    #
    # def do_insert(self, cursor, item):
    #     insert_sql, params = item.get_insert_sql()
    #     cursor.execute(insert_sql, params)