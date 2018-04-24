# -*- coding: utf-8 -*-
"""
Title = 全书网全站小说下载
Date = 20180423
"""
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
        for novel_list in response.xpath("//ul[@class='seeWell cf']/li/span/a"):
            novel_title = novel_list.xpath('@title').extract_first()    # 小说名
            novel_url = novel_list.xpath('@href').extract_first('')     # 小说地址
            if novel_title is None:
                continue

            yield scrapy.Request(novel_url, callback=self.parse_novel_url)

        # 判断是否存在下一页
        next_url = response.xpath("//*[@id='pagelink']/a[@class='next']/@href").extract_first()
        if next_url != "":
            yield scrapy.Request(next_url, callback=self.parse_novel_type_url)

    # 解析小说
    def parse_novel_url(self, response):
        novel_book_url = response.xpath("//div[@class='b-oper']/a[1]/@href").extract_first()
        yield scrapy.Request(novel_book_url, callback=self.parse_book)

    # 解析小说的每个章节
    def parse_book(self, response):
        for item in response.xpath("//div[@class='clearfix dirconone']//li/a"):

            book_url = item.xpath('@href').extract_first()
            print(book_url)
            yield scrapy.Request(book_url, callback=self.save_book)

    # 获取每章节的小说
    def save_book(self, response):
        demo_item = DemoItem()
        book_context = ''
        for book_context_ in response.xpath('//div[@class="mainContenr"]/text()').extract():    # 小说内容:
            if book_context_ == '\r' or book_context_ == '\r\n' or book_context_ == '&nbsp;':
                book_context_ = ''
            book_context += book_context_
        demo_item['novel_name'] = response.xpath('//*[@id="directs"]/div[1]/h1/em/text()').extract_first()  # 小说名
        demo_item['book_name'] = response.xpath('//*[@id="directs"]/div[1]/h1/strong/text()').extract_first()   # 章节名
        demo_item['book_url'] = response.url    # 章节地址
        demo_item['book_context'] = book_context
        yield demo_item
