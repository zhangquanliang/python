# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    novel_name = scrapy.Field()  # 小说名
    book_name = scrapy.Field()  # 小说章节名
    book_url = scrapy.Field()  # 小说章节地址
    book_context = scrapy.Field()   # 小说内容
    pass
