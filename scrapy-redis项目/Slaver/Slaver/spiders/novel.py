# -*- coding: utf-8 -*-
import scrapy
from ..items import SlaverItem
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup


class NovelSpider(RedisSpider):
    name = 'novel'
    # allowed_domains = ['novel.com']
    redis_key = 'novel_url'

    def parse(self, response):
        url = response.xpath('//*[@id="container"]/div[2]/section/div/div[1]/div[2]/a[1]/@href').extract_first()
        yield scrapy.Request(url, callback=self.parse_chapter)

    def parse_chapter(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_type_list = soup.find_all('div', class_='clearfix dirconone')
        print(len(chapter_type_list))
        for chapter_type in chapter_type_list:
            chapter_list = chapter_type.find_all('li')
            for chapter_ in chapter_list:
                url = chapter_.find('a')['href']
                title = chapter_.find('a').get_text()
                print('获取章节[{}], 地址[{}]成功..'.format(title, url))
                yield scrapy.Request(url, callback=self.parse_novel)

    def parse_novel(self, response):
        item = SlaverItem()
        chapter_url = response.url
        novel_type = response.xpath('//*[@id="direct"]/a[2]/text()').extract_first()
        novel_name = response.xpath('//*[@id="direct"]/a[3]/text()').extract_first()
        chapter_name = str(response.xpath('//*[@id="direct"]/text()[4]').extract_first()).replace(' ', '').replace('> ',
                                                                                                                   '').replace(
            '章 ', '').replace('节', '').replace('目', '').replace('录', '').strip()
        context_list = response.xpath('//*[@id="content"]/text()').extract()
        context = str(context_list).replace('\xa0', '').replace('\r', '').replace('\n', '').replace('[', '').replace(
            ']', '').replace("'", '')
        item['chapter_url'] = chapter_url
        item['novel_type'] = novel_type
        item['novel_name'] = novel_name
        item['chapter_name'] = chapter_name
        item['context'] = context
        yield item
