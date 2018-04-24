# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class Demo2Pipeline(object):
    def process_item(self, item, spider):
        book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
        sheet = book.add_sheet("Sheet")  # 添加Excel页签
        sheet.write_merge(0, 0, 0, 7, '豆瓣热门电影')
        sheet.write(1, 0, '电影名')
        sheet.write(1, 1, '电影评分')
        sheet.write(1, 2, '电影地址')
        sheet.write(1, 3, '封面地址')
        print('长度为', len(item))
        for i in range(len(item)):
            sheet.write(i+2, 0, item['name'])
            sheet.write(i+2, 1, item['rate'])
            sheet.write(i+2, 2, item['url'])
            sheet.write(i+2, 3, item['image_url'])
        path = r'豆瓣热门.xls'
        book.save(path)
        return item
