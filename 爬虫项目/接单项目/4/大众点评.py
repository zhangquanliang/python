# -*- coding:utf-8 -*-
__author__ = 'zhangql'
__title__ = '大众点评'
import requests
from openpyxl import Workbook
import re
import time
book = Workbook()
sheet = book.create_sheet('大众点评')
sheet.append(['省份', '城市', '区县', '门店名称', '地址', '电话', '人均消费', '点评数量', '产品点评打分', '环境点评打分', '服务点评打分'])
from bs4 import BeautifulSoup
headers = {
        "Cookie": "_lxsdk_cuid=163edb15be0c8-0b969493143529-4d015463-100200-163edb15be175; _lxsdk=163edb15be0c8-0b969493143529-4d015463-100200-163edb15be175; _hc.v=4b1412ae-fe14-90f4-a9a5-5df95a27fa6b.1528701214; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1528701273; cy=7; cye=shenzhen; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; s_ViewType=10; _lxsdk_s=164d9b926d6-026-5fc-2d9%7C%7C99",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "Upgrade-Insecure-Requests":"1"
    }

shop_url_list = []


# 传入每页的地址，获取到详情页的地址
def get_detail_url(page_url):
    response = requests.get(page_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        shop_list = soup.find_all('div', class_='operate J_operate Hide')
        for shop_ in shop_list:
            detal_url = shop_.find('a')['href'].replace('/review', '')
            if detal_url in shop_url_list:
                continue
            print(page_url, detal_url)
            shop_url_list.append(detal_url)
    else:
        print('请求异常，请确认响应地址[{}]'.format(page_url))


# 获取每个店铺的相关信息，进行数据处理，写入Excel
def get_detail(url):
    html = ''
    for i in range(3):
        html = requests.get(url, headers=headers).text
        if '验证中心' in html:
            time.sleep(40)
            print('需要输入验证码，请40秒内点击，然后重试。')
            continue
        else:
            break
    parse_detail(html)  # 传入需要解析的详情页面


# 传入一个初始地址，获取到下一页的地址
def get_shop_url(url):
    response1 = requests.get(url, headers=headers)
    if response1.status_code == 200:
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        # 通过查找区来分开，对每个区进行查询，得到数据
        for nav in soup1.find('div', id='region-nav').find_all('a'):
            # 取每个区的地址，进行查询
            area_url = nav['href']  # 每个区的第一页
            area_name = nav['data-click-title']
            response2 = requests.get(area_url, headers=headers)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            try:
                page_url = soup2.find('a', class_='next')['href']
            except:
                page_url = 0
            print(area_name, '当前地址 ', area_url, '下一页地址', page_url)
            get_detail_url(area_url)    # 传入每一页的地址
            if page_url:
                get_next_page(page_url)
    else:
        print(response1.status_code, response1.url)
        print('初始化地址，请求异常，请确认响应地址[{}]'.format(url))


# 传入下一页的地址，继续回调请求下一页
def get_next_page(page_url):
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    get_detail_url(page_url)  # 传入每一页的地址
    try:
        next_url = soup.find('a', class_='next')['href']
    except:
        next_url = 0
    if next_url:
        get_next_page(next_url)


# 解析详情页面，写入Excel
def parse_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        area1 = soup.find('div', class_='breadcrumb').find_all('a')[-2].get_text()
    except:
        area1 = ''
    try:
        area2 = soup.find('div', class_='breadcrumb').find_all('a')[-1].get_text()
    except:
        area2 = ''
    area = area1 + ' ' + area2  # 区县
    try:
        title = soup.find('div', class_='breadcrumb').find('span').get_text()  # 门店名称
    except:
        title = '-'
    try:
        address = re.findall('shopName: ".*?", address: "(.*?)", publicTransit: "",', str(html), re.I | re.S)[0]
    except:
        address = '-'
    try:
        phone = soup.find('p', class_='expand-info tel').get_text().replace('电话：', '').replace('添加', '')  # 电话
    except:
        phone = ''
    try:
        avgPriceTitle = soup.find('span', id='avgPriceTitle').get_text().replace('消费:', '')  # 消费
    except:
        avgPriceTitle = 15
    try:
        reviewCount = soup.find('span', id='reviewCount').get_text().replace('条评论', '')  # 评论
    except:
        reviewCount = 7
    try:
        product_scoring = \
        re.findall('<span class=".*">产品:(.*?)</span>', str(soup.find('span', id='comment_score')), re.S | re.I)[0]
    except:
        product_scoring = 7.2
    try:
        environmental_scoring = \
        re.findall('<span class=".*">环境:(.*?)</span>', str(soup.find('span', id='comment_score')), re.S | re.I)[0]
    except:
        environmental_scoring = 7.2
    try:
        service_scoring = \
        re.findall('<span class=".*">服务:(.*?)</span>', str(soup.find('span', id='comment_score')), re.S | re.I)[0]
    except:
        service_scoring = 7.2
    print('采集到的数据为: ', area, title, address, phone, avgPriceTitle, reviewCount, product_scoring, environmental_scoring,
          service_scoring)
    sheet.append(
        ['浙江', '嘉兴', area, title, address, phone, avgPriceTitle, reviewCount, product_scoring, environmental_scoring,
         service_scoring])


if __name__ == '__main__':
    url = 'https://www.dianping.com/search/keyword/102/0_全家便利店'
    get_shop_url(url)
    for shop_url in shop_url_list:
        get_detail(shop_url)
    book.save('大众点评-嘉兴1.xlsx')
