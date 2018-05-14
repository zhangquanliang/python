# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    houseIcon = scrapy.Field()  # 房屋信息
    positionInfo = scrapy.Field()  # 位置信息
    totalPrice = scrapy.Field()   # 总价
    unitPrice = scrapy.Field()  # 单价
    tag = scrapy.Field()  # 房屋标签
    house_url = scrapy.Field()  # 房屋地址