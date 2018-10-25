# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SlaverItem(scrapy.Item):
    # define the fields for your item here like:
    chapter_url = scrapy.Field()    # 章节地址
    novel_type = scrapy.Field()  # 小说类型
    novel_name = scrapy.Field()  # 小说名字
    chapter_name = scrapy.Field()   # 章节名字
    context = scrapy.Field()    # 章节内容
    # pass
