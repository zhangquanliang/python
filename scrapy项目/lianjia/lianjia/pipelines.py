# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from scrapy项目.lianjia.lianjia import settings
pymysql.install_as_MySQLdb()


class LianjiaPipeline(object):
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
            title = item['title']
            houseIcon = item['houseIcon']
            positionInfo = item['positionInfo']
            totalPrice = item['totalPrice']
            unitPrice = item['unitPrice']
            tag = item['tag']
            house_url = item['house_url']
            self.db_insert(title, houseIcon, positionInfo, totalPrice, unitPrice, tag, house_url)
        except  Exception as e:
            print('输入插入异常，请确认！')
        return item

    def db_insert(self, title, houseIcon, positionInfo, totalPrice, unitPrice, tag, house_url):
        create_time = create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into lianjia(title, houseIcon, positionInfo, totalPrice, unitPrice, tag, house_url, create_time)" \
              "values('{}', '{}', '{}', '{}','{}', '{}','{}', '{}')"\
            .format(title, houseIcon, positionInfo, totalPrice, unitPrice, tag, house_url, create_time)
        self.cursor.execute(sql)
        self.connect.commit()

    def db_close(self):
        self.cursor.close()
        self.connect.close()