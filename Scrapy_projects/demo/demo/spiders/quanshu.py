# -*- coding: utf-8 -*-
"""全书网全站小说下载"""
import scrapy
from ..items import DemoItem


class BaiduSpider(scrapy.Spider):
    name = 'quanshu'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/']

    def parse(self, response):
        novel_type_url_list = response.xpath("//ul[@class='channel-nav-list']/li/a/@href").extract()  # 获取到不同类型的小说地址
        for novel_type_url in novel_type_url_list:
            yield scrapy.Request(novel_type_url, callback=self.parse_novel_type_url)

    # 解析不同类型的所有小说
    def parse_novel_type_url(self, response):
        novel_url_list = response.xpath("//ul[@class='seeWell cf']//li/a/@href").extract()    # 获取所有小说的地址
        for novel_url in novel_url_list:
            yield scrapy.Request(novel_url, callback=self.parse_novel_url)

        # 判断是否存在下一页
        next_url = response.xpath("//*[@id='pagelink']/a[@class='next']/@href").extract_first()
        if next_url != "":
            yield scrapy.Request(next_url, callback=self.parse_novel_type_url)

    # 解析小说
    def parse_novel_url(self, response):
        nover_book_url = response.xpath("//div[@class='b-oper']/a[1]/@href").extract_first()
        yield scrapy.Request(nover_book_url, callback=self.parse_book)

    # 解析小说的每个章节
    def parse_book(self, response):
        for item in response.xpath("//div[@class='clearfix dirconone']//li/a"):

            demoitem = DemoItem()
            book_name = item.xpath('text()').extract()
            book_url = item.xpath('@href').extract()
            demoitem['book_name'] = book_name
            demoitem['book_url'] = book_url

            yield demoitem