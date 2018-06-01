# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BosszpItem(scrapy.Item):
    # define the fields for your item here like:
    zp_name = scrapy.Field()
    gsdz = scrapy.Field()
    date = scrapy.Field()
    pass
