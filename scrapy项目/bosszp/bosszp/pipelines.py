# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class BosszpPipeline(object):
    wb = Workbook()
    ws = wb.active
    ws.append(['招聘人', '公司地址', '最近招聘日期'])

    def process_item(self, item, spider):
        line = [item['zp_name'], item['gsdz'], item['date']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('boss直聘.xlsx')  # 保存xlsx文件
        return item
