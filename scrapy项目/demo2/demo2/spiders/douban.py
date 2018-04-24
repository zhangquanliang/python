# -*- coding: utf-8 -*-
"""
Title = 豆瓣热门
Date = 20180423
"""
import scrapy
import json
import xlwt


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=1200&page_start=0']

    def parse(self, response):
        data = json.loads(response.text)['subjects']
        book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
        sheet = book.add_sheet("Sheet")  # 添加Excel页签
        sheet.write_merge(0, 0, 0, 7, '豆瓣热门电影')
        sheet.write(1, 0, '电影评分')
        sheet.write(1, 1, '电影名')
        sheet.write(1, 2, '电影地址')
        sheet.write(1, 3, '封面地址')
        for i in range(len(data)):
            sheet.write(i + 2, 0, data[i]['rate'])
            sheet.write(i + 2, 1, data[i]['title'])
            sheet.write(i + 2, 2, data[i]['url'])
            sheet.write(i + 2, 3, data[i]['cover'])
            for j in range(4):
                sheet.col(j).width = 0x0d00 + j * 600
        path = r'豆瓣热门.xls'
        book.save(path)