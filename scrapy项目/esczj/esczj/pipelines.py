# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
pymysql.install_as_MySQLdb()
import os, sys
sys.path.append(os.path.dirname(__file__))
import datetime
import settings


class EsczjPipeline(object):
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
            create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into esczj (car_series, car_id, models, price, travel_mileage, last_time, displacement, city, standard, " \
                  "car_location, contacts, inspection_expires, insurance_expires, warranty_expires, emission_standard," \
                  " number_of_transfers, cer_user, maintenance, merchant_name, cer_engine, transmission, vehicle_class, color," \
                  " fuel_label, drive_type, mouth, create_date)" \
                  " values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'," \
                  " '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(item['car_series'], item['car_id'], item['models'], item['price'], item['travel_mileage'], item['last_time'], item['displacement'],
                      item['city'], item['standard'], item['car_location'], item['contacts'], item['inspection_expires'],
                      item['insurance_expires'], item['warranty_expires'], item['emission_standard'], item['number_of_transfers'],
                      item['cer_user'], item['maintenance'], item['merchant_name'], item['cer_engine'], item['transmission'],
                      item['vehicle_class'], item['color'], item['fuel_label'], item['drive_type'], item['mouth'], create_date)
            self.db_insert(sql)
        except Exception as e:
            print('输入插入异常，请确认！', e)
        return item

    def db_insert(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def db_close(self):
        self.cursor.close()
        self.connect.close()