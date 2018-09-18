# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SlaverPipeline(object):
    def process_item(self, item, spider):
        with open('novel.txt', 'a+', encoding='utf-8') as f:
            f.write('小说类型:{}, 作者: {}'.format(item['novel_type'], item['author']) + '\n')
        return item
