# -*- coding: utf-8 -*-
import scrapy
from ..items import MasteItem
from scrapy_redis.spiders import RedisSpider


class DingdianSpider(RedisSpider):
    name = 'dingdian'
    # start_urls = ['https://www.23us.so/list/2_1.html']

    redis_key = "novel"

    def parse(self, response):
        novel_list = response.xpath('//*[@id="content"]/dd[1]/table//tr')
        for novel in novel_list:
            item = MasteItem()
            novel_url = novel.xpath('td[1]/a/@href').extract()
            if len(novel_url) == 0:
                continue
            item['novel_url'] = novel_url[0]
            yield item
