# -*- coding: utf-8 -*-
import scrapy
import re
import csv
from bs4 import BeautifulSoup
import os, sys
sys.path.append(os.path.dirname(__file__))
from ..items import EsczjItem


class ExampleSpider(scrapy.Spider):
    name = 'esczj'
    allowed_domains = ['che168.com']
    start_url_list = []
    with open('车系.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            if item[1] == '车系地址':
                continue
            start_url_list.append(item[1])
    start_urls = start_url_list

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        if 'fn-clear certification-list' not in response.text:
            return
        li_list = soup.find('ul', class_='fn-clear certification-list').find_all('li')
        for li in li_list:
            if 'target' in str(li):
                url = 'https://www.che168.com' + li.find('a', target='_blank')['href']
                yield scrapy.Request(url, callback=self.parse_html)
            else:
                continue
        if 'page-item-next' not in response.text:
            return
        next_page = 'https://www.che168.com' + soup.find('a', class_='page-item-next')['href']
        if next_page is None:
            return
        print('下一页', next_page)
        yield scrapy.Request(next_page, callback=self.parse)

    def parse_html(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 车辆信息
        try:
            car_series = soup.find('div', class_='breadnav content').find_all('a')[4].get_text().replace('二手', '')
        except:
            car_series = ''
        car_id = soup.find('input', id='car_specid')['value']
        models = soup.find('div', class_='car-info').find('h2').get_text().replace(" ", '')  # 车型
        price = soup.find('div', class_='car-info').find('div', class_='car-price').find('ins').get_text().replace('￥', '') # 价格
        travel_mileage = soup.find('div', class_='details').find_all('li')[0].find('span').get_text().replace('万公里', '')  # 行驶里程
        last_time = soup.find('div', class_='details').find_all('li')[1].find('span').get_text()  # 上牌时间
        displacement = soup.find('div', class_='details').find_all('li')[2].find('span').get_text()  # 排量
        city = soup.find('div', class_='details').find_all('li')[3].find('span').get_text()  # 所在地

        standard_name = soup.find('div', class_='details').find_all('li')[4].find('span').get_text()  # 标准名字
        # standard_url = 'https://www.che168.com' + soup.find('div', class_='details').find_all('li')[4].find('a')['href']   # 标准地址
        standard = standard_name  # 标准
        car_address = soup.find('div', class_='car-address')   # 车辆信息
        try:
            car_location = re.findall('看车地点.(.*?)<br/>联系人', str(car_address), re.I | re.S)[0].replace('\n', '').strip()  # 看车地点
        except:
            car_location = "-"
        try:
            contacts = re.findall('联系人.(.*?)发布时间', str(car_address), re.I | re.S)[0].replace('\n', '').strip()  # 联系人
        except:
            contacts = "-"
        # 基本信息
        inspection_expires = soup.find('div', id='anchor01').find_all('li')[0].get_text().replace('年检到期：', '')  # 年检到期
        insurance_expires = soup.find('div', id='anchor01').find_all('li')[1].get_text().replace('保险到期：', '')  # 保险到期
        warranty_expires = soup.find('div', id='anchor01').find_all('li')[2].get_text().replace('质保到期：', '')  # 质保到期
        emission_standard = soup.find('div', id='anchor01').find_all('li')[3].get_text().replace('排放标准：', '')  # 排放标准
        number_of_transfers = soup.find('div', id='anchor01').find_all('li')[4].get_text().replace('过户次数：', '')  # 过户次数
        cer_user = soup.find('div', id='anchor01').find_all('li')[5].get_text().replace(" ", '').replace('用　　途：', '')  # 用途
        maintenance = soup.find('div', id='anchor01').find_all('li')[6].get_text().replace('维修保养：', '')  # 维修保养
        merchant_name_ = soup.find('div', id='anchor01').find_all('li')[7]  # 商家名称
        try:
            merchant_name = re.findall('<span>商家名称.</span>(.*?)<a', str(merchant_name_), re.S | re.I)[0].strip()
        except:
            merchant_name = "-"
        # 车辆配置
        cer_engine = soup.find('div', id='anchor02').find_all('li')[0].get_text().replace(" ", '').replace('发动机：', '')   # 发动机
        transmission = soup.find('div', id='anchor02').find_all('li')[1].get_text().replace(" ", '').replace('变速器：', '')   # 变速器
        vehicle_class = soup.find('div', id='anchor02').find_all('li')[2].get_text().replace('车辆级别：', '')   # 车辆级别
        color = soup.find('div', id='anchor02').find_all('li')[3].get_text().replace(" ", '').replace('颜　　色：', '')   # 颜色
        fuel_label = soup.find('div', id='anchor02').find_all('li')[4].get_text().replace('燃油标号：', '')   # 燃油标号
        drive_type = soup.find('div', id='anchor02').find_all('li')[5].get_text().replace('驱动方式：', '')   # 驱动方式
        mouth = soup.find('div', id='anchor02').find_all('li')[6].get_text().replace('查看详情', '').replace('车型口碑：', '') .strip()  # 车型口碑

        esczj = EsczjItem()
        esczj['car_series'] = car_series
        esczj['car_id'] = car_id
        esczj['models'] = models
        esczj['price'] = price
        esczj['travel_mileage'] = travel_mileage
        esczj['last_time'] = last_time
        esczj['displacement'] = displacement
        esczj['city'] = city
        esczj['standard'] = standard
        esczj['car_location'] = car_location
        esczj['contacts'] = contacts
        esczj['inspection_expires'] = inspection_expires
        esczj['insurance_expires'] = insurance_expires
        esczj['warranty_expires'] = warranty_expires
        esczj['emission_standard'] = emission_standard
        esczj['number_of_transfers'] = number_of_transfers
        esczj['cer_user'] = cer_user
        esczj['maintenance'] = maintenance
        esczj['merchant_name'] = merchant_name
        esczj['cer_engine'] = cer_engine
        esczj['transmission'] = transmission
        esczj['vehicle_class'] = vehicle_class
        esczj['color'] = color
        esczj['fuel_label'] = fuel_label
        esczj['drive_type'] = drive_type
        esczj['mouth'] = mouth
        yield esczj
