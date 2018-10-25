# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy_splash import SplashRequest
import scrapy_splash

"""常规的Scrapy格式"""


class ExampleSpider(scrapy.Spider):
    name = 'blbl'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/']

    def start_requests(self):
        for url in self.start_urls:
            # headers = {
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
            # }
            yield SplashRequest(url, callback=self.parse_result)

    def parse_result(self, response):
        logging.info('====================================================')
        content = response.xpath("//div[@class='num-wrap']").extract_first()
        logging.info(content)
        logging.info('====================================================')

# class splash(scrapy.Spider):
#     name = "blbl"
#     allowed_domains = ["bilibili.com"]
#     start_urls = [
#         "https://www.bilibili.com/"
#     ]
#
#     def start_requests(self):
#         splash_args = {
#             'wait': '5',
#         }
#         for url in self.start_urls:
#             yield SplashRequest(url, self.parse_result, args=splash_args, endpoint='render.html')
#
#     def parse_result(self, response):
#         logging.info('====================================================')
#         content = response.xpath("//div[@class='num-wrap']").extract_first()
#         logging.info(content)
#         logging.info('====================================================')
