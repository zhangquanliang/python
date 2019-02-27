# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BulletsPipeline(object):
    def process_item(self, item, spider):
        month = item['month']
        text = item['text']
        file_name = str(month) + '_goods.txt'
        f = open(file_name, 'a', encoding='utf_8')
        f.write(text + '\n')
        f.close()
        return item
