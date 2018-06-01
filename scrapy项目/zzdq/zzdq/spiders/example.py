# -*- coding: utf-8 -*-
import scrapy
import pymysql
import requests
import datetime
pymysql.install_as_MySQLdb()
from bs4 import BeautifulSoup


class ExampleSpider(scrapy.Spider):
    name = 'zzdq'
    allowed_domains = ['jb39.com']
    start_urls = ['http://jb39.com/zhengzhuang/zhengzhuang-all.htm']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_list = soup.find_all('ul', class_='post-mulu')[0]
        for li in ul_list.find_all('li'):
            symptom_url = 'http://jb39.com' + li.find('a')['href']
            yield scrapy.Request(symptom_url, callback=self.get_symptom_context)

    # 入口函数
    def get_symptom_context(self, response):
        self.parser_html(response.text)

    # 解析入口函数返回的数据包
    def parser_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            mingchen = soup.find('h2', class_='h2-gr jb-search').get_text()  # 名称
        except:
            mingchen = soup.find('h1', class_='post-title').get_text()  # 名称
        try:
            bieming = soup.find('span', class_='spider').get_text()  # 别名
        except:
            bieming = ""
        try:
            jianjie = soup.find('p', class_='zz-body').get_text()  # 简介
        except:
            jianjie = ""
        try:
            bingyin_url = 'http://jb39.com' + soup.find('h2', class_='jb-h2 zz-by-index').find('a')['href']  # 病因全部地址
            bingyin = self.parser_more(bingyin_url)
        except:
            bingyin = ""
        try:
            jiancha_url = 'http://jb39.com' + soup.find('h2', class_='jb-h2 zz-jc-index').find('a')['href']  # 检查全部地址
            jiancha = self.parser_more(jiancha_url)
        except:
            jiancha = ""
        try:
            zhenduan_url = 'http://jb39.com' + soup.find('h2', class_='jb-h2 zz-zd-index').find('a')['href']  # 诊断全部地址
            zhenduan = self.parser_more(zhenduan_url)
        except:
            zhenduan = ""
        try:
            buwei_list = soup.find('ul', class_='ul-ss-3 zz-xx-bw').find_all('li')  # 症状部位
            buwei = self.get_zz(buwei_list)
        except:
            buwei = ""
        try:
            keshi_list = soup.find('ul', class_='ul-ss-3 zz-xx-ks').find_all('li')  # 症状科室
            keshi = self.get_zz(keshi_list)
        except:
            keshi = ""
        try:
            zhengzhuan_list = soup.find('ul', class_='ul-ss-3 zz-xx-zz').find_all('li')  # 相关症状
            zhengzhuan = self.get_zz(zhengzhuan_list)
        except:
            zhengzhuan = ""
        try:
            jibing_list = soup.find('ul', class_='ul-ss-3 zz-xx-jb').find_all('li')  # 相关疾病
            jibing = self.get_zz(jibing_list)
        except:
            jibing = ""
        try:
            zzjiancha_list = soup.find('ul', class_='ul-ss-3 zz-xx-jc').find_all('li')  # 症状检查
            zzjiancha = self.get_zz(zzjiancha_list)
        except:
            zzjiancha = ""
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if '男' in jianjie or '男' in bingyin or '男' in jiancha or '男' in zhenduan or '男' in buwei\
                or '男' in zhengzhuan or '男' in zzjiancha or '男' in jibing:
            xiangguanrq = '男人'
        elif '女' in jianjie or '女' in bingyin or '女' in jiancha or '女' in zhenduan or '女' in buwei\
                or '女' in zhengzhuan or '女' in zzjiancha or '女' in jibing:
            xiangguanrq = '女人'
        else:
            xiangguanrq = '所有人群'
        sql = "insert into zzdq(mingchen, bieming, jianjie, bingyin, jiancha, zhenduan, buwei, keshi, zhengzhuan," \
              " jibing, zzjiancha, xiangguanrq,create_date) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')" \
            .format(mingchen, bieming, jianjie, bingyin, jiancha, zhenduan, buwei, keshi, zhengzhuan, jibing, zzjiancha,
                    xiangguanrq, create_date)
        try:
            self.db_insert(sql)
            print('症状[{}], 别名[{}], 入库成功！'.format(mingchen, bieming))
        except Exception as ex:
            print('入库异常! {}'.format(ex))

    # 数据库连接入库
    def db_insert(self, sql):
        conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='dianshang', charset='utf8')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    # 对病因, 检查，诊断数据数据采集全部做处理
    def parser_more(self, url):
        response = requests.get(url)
        response.encoding = 'gbk'
        bysoup = BeautifulSoup(response.text, 'html.parser')
        result = bysoup.find('div', class_='spider').get_text().strip()
        return result

    def get_zz(self, zz_list):
        if len(zz_list) == 1:
            return zz_list[0].find('a').get_text()
        result = ""
        for i in zz_list:
            s = i.find('a').get_text()
            result += s + "$"
        return result[:-1]