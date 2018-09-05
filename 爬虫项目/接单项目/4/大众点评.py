# -*- coding:utf-8 -*-
__author__ = 'zhangql'
__title__ = '大众点评'
import requests
from openpyxl import Workbook
import re
import time
book = Workbook()
sheet = book.create_sheet('大众点评')
sheet.append(['省份', '城市', '区县', '门店名称', '地址', '电话'])
# sheet.append(['省份', '城市', '区县', '门店名称', '地址', '电话', '人均消费', '点评数量', '产品点评打分', '环境点评打分', '服务点评打分'])

from bs4 import BeautifulSoup
headers = {
        "Cookie": "_lxsdk_cuid=165a247080a1f-09689588478247-4d015463-100200-165a247080bc8; _lxsdk=165a247080a1f-09689588478247-4d015463-100200-165a247080bc8; _hc.v=e72e528f-b7d0-9ce3-dc0f-16faef8953e8.1536025889; _thirdu.c=4e5d8a2390b183e2af2d7078c3301460; thirdtoken=68B69EB069519FA1E2C823DCF3BD4480; JSESSIONID=F3061A01570DF13E8DB31C4F7204FE87; _dp.ac.v=a1c149c2-0d8e-441c-a99d-fae9de5168e8; dper=457595f486de7fd607d63b70b8ba27b299a50057c1d33b9b242fdaca292799bfc06c3caf1fdbd9f66ed7b39037df6dcbb04a8045c23525f062c14320a2173f0d179f4f257f13115c50b396b76503c2bb17bf4df7670dbf86864540da47e2ef7c; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3935931626; ctu=cb90e491e3f15f0564c9497c7f499eb860e504abdc60cc1034c7f996d690aea7; uamo=15179833772; s_ViewType=10; wed_user_path=27809|0; aburl=1; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __utma=1.327481792.1536156599.1536156599.1536156599.1; __utmb=1.3.10.1536156599; __utmc=1; __utmz=1.1536156599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _lxsdk_s=165aa0f27b8-26f-805-039%7C%7C269",
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
            break
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
    area = area1 + '' + area2  # 区县
    try:
        title = soup.find('div', class_='breadcrumb').find('span').get_text()  # 门店名称
    except:
        title = '-'
    try:
        address = re.findall('shopName: ".*?", address: "(.*?)", publicTransit: ".*?",', str(html), re.I | re.S)[0]
    except:
        address = '-'
    try:
        phone = soup.find('p', class_='expand-info tel').get_text().replace('电话：', '').replace('添加', '')  # 电话
    except:
        phone = ''
    # try:
    #     avgPriceTitle = soup.find('span', id='avgPriceTitle').get_text().replace('消费:', '')  # 消费
    # except:
    #     avgPriceTitle = 15
    # try:
    #     reviewCount = soup.find('span', id='reviewCount').get_text().replace('条评论', '')  # 评论
    # except:
    #     reviewCount = 7
    # try:
    #     product_scoring = \
    #     re.findall('<span class=".*">产品:(.*?)</span>', str(soup.find('span', id='comment_score')), re.S | re.I)[0]
    # except:
    #     product_scoring = 7.2
    # try:
    #     environmental_scoring = \
    #     re.findall('<span class=".*">环境:(.*?)</span>', str(soup.find('span', id='comment_score')), re.S | re.I)[0]
    # except:
    #     environmental_scoring = 7.2
    # try:
    #     service_scoring = \
    #     re.findall('<span class=".*">服务:(.*?)</span>', str(soup.find('span', id='comment_score')), re.S | re.I)[0]
    # except:
    #     service_scoring = 7.2
    # print('采集到的数据为: ', area, title, address, phone, avgPriceTitle, reviewCount, product_scoring, environmental_scoring,
    #       service_scoring)
    print('采集到的数据为: ', area, title, address, phone)
    sheet.append(
        ['上海', '上海', area, title, address, phone])


if __name__ == '__main__':
    url = 'https://www.dianping.com/search/keyword/1/0_英式'
    get_shop_url(url)
    for shop_url in shop_url_list:
        get_detail(shop_url)
        break
    book.save('大众点评-上海.xlsx')
