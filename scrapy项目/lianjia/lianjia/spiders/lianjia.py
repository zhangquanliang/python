# -*- coding: utf-8 -*-
"""
Title = 深圳地区链家二手房
Date = 20180511
"""
import scrapy
import re


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['sz.lianjia.com']
    start_urls = ['https://sz.lianjia.com/ershoufang/']

    def parse(self, response):
        page_text = response.xpath("//div[@class='page-box house-lst-page-box']").extract_first()
        page = re.findall('{"totalPage":(.*?),"curPage":1}', page_text, re.I | re.S)[0]
        for i in range(1, int(page)+1):
            url = 'https://sz.lianjia.com/ershoufang/pg{}/'.format(i)
            yield scrapy.Request(url, callback=self.get_html)

    def get_html(self, response):
        from ..items import LianjiaItem
        item = LianjiaItem()
        title_ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[1]/a/text()").extract()
        houseIcon__ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[2]/div[1]/a/text()").extract()
        houseIcon_ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[2]/div[1]/text()").extract()
        positionInfo__ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[3]/div[1]/text()").extract()
        positionInfo_ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[3]/div[1]/a/text()").extract()
        totalPrice__ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[6]/div[1]/span/text()").extract()
        totalPrice_ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[6]/div[1]/text()").extract()
        unitPrice_ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[6]/div[2]/span/text()").extract()
        tag_ = response.xpath("//ul[@class='sellListContent']/li/div[@class='info clear']/div[5]").extract()
        house_url_ = response.xpath("//ul[@class='sellListContent']//li/a/@href").extract()
        for i in range(len(house_url_)):
            title = title_[i]
            houseIcon = houseIcon__[i] + houseIcon_[i]
            positionInfo = positionInfo__[i] + positionInfo_[i]
            totalPrice = totalPrice__[i] + totalPrice_[i]
            unitPrice = unitPrice_[i]
            tag = ""
            reg = re.findall('<span class=".*?">(.*?)</span>', str(tag_[i]))
            for j in range(len(reg)):
                tag += reg[j] + '-'
            house_url = house_url_[i]
            item['title'] = title
            item['houseIcon'] = houseIcon
            item['positionInfo'] = positionInfo
            item['totalPrice'] = totalPrice
            item['unitPrice'] = unitPrice
            item['tag'] = tag
            item['house_url'] = house_url
            yield item
