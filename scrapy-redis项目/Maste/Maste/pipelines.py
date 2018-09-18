# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
r = redis.Redis(host='120.55.48.59', port=6379)


class MastePipeline(object):
    def process_item(self, item, spider):
        r.lpush('novel_url', item['novel_url'])
        return item
