# -*- coding: utf-8 -*-
import scrapy
import pymysql
import requests
import datetime
import time
pymysql.install_as_MySQLdb()
from bs4 import BeautifulSoup


class ExampleSpider(scrapy.Spider):
    name = '58job'
    # allowed_domains = ['qd58.com']
    # 添加其它职位的，只需要把服务器替换成其它就好，如：http://qd.58.com/job/?key=网管&final=1&jump=1
    start_urls = ['http://qd.58.com/job/?key=服务员&final=1&jump=1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list = soup.find_all('div', class_='job_name clearfix')
        for job_ in job_list:
            job_url = job_.find('a')['href']
            yield scrapy.Request(job_url, callback=self.parse_job)
            print('job_url', job_url)
        try:
            next_url = soup.find('div', class_='pagesout').find('a', class_='next')['href']
        except Exception as ex:
            print('解析异常，原因为：{}'.format(ex))
            return
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_job(self, response):
        if '频繁' in response.text:
            print('请求过于频繁, 需要手动确定验证码，等待120秒重试...')
            time.sleep(120)
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('span', class_='pos_title').get_text().strip()
        address = soup.find('span', class_='pos_area_span pos_address').get_text().replace(' ', '')
        salary = soup.find('span', class_='pos_salary').get_text().strip()
        url = response.url
        city = soup.find('span', class_='zp_crumb').find('a', class_='crumb_item').get_text().replace('58同城', '').strip()
        claim = soup.find('div', class_='pos_base_condition').get_text().strip()
        welfare = soup.find('div', class_='posDes').get_text().strip()
        # if '福利' or '待遇' not in welfare:
        #     welfare = ''
        # else:
        #     welfare = welfare
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into 58job(title, address, salary, url, city, claim, welfare, create_date)" \
              " values ('{}', '{}', '{}','{}', '{}', '{}','{}', '{}')".\
            format(title, address, salary, url, city, claim, welfare, create_date)
        print(sql)
        self.db_insert(sql=sql)
        print('保存职位:{}成功...其它信息为:'.format(title), address, salary, url, city, claim, welfare)

    # 数据库连接入库
    def db_insert(self, sql):
        # 修改成自己的mysql数据库连接。
        conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='spider_j',
                               charset='utf8')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()