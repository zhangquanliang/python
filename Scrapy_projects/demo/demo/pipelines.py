# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DemoPipeline(object):
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
    def process_item(self, item, spider):
        with open('qswbook.txt', 'a', encoding='utf-8') as f:
            book_names = item['book_name']
            book_urls = item['book_url']
            for i, j in zip(book_names, book_urls):
                f.write(i + ':' + j + '\n')
            f.close()
        return item