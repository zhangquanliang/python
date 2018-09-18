# -*- coding:utf-8 -*-
__author__ = 'zhangql'
__title__ = '大众点评'
import requests
from openpyxl import Workbook
import re
import time
book = Workbook()
sheet = book.create_sheet('大众点评')
sheet.append(['省份', '城市', '区县', '门店名称', '地址', '总评论数', '店铺星级', '评论'])
# sheet.append(['省份', '城市', '区县', '门店名称', '地址', '电话', '人均消费', '点评数量', '产品点评打分', '环境点评打分', '服务点评打分'])
result = ''


from bs4 import BeautifulSoup
headers = {
        "Cookie": "_lxsdk_cuid=165ac83ae18c8-0742f9d07d6d42-4d015463-1fa400-165ac83ae18c8; _lxsdk=165ac83ae18c8-0742f9d07d6d42-4d015463-1fa400-165ac83ae18c8; _hc.v=2a3bcd6d-6597-149a-22a4-dbc121a8a439.1536197636; lgtoken=06babea71-7d4a-49b3-83db-bc5d90b0fbfc; dper=457595f486de7fd607d63b70b8ba27b244b8c512d68d61a27c20124893dc02059af9a7dbb1144c362ff274c97a6b6b67e40acd663e97edcb729c272a704f195d0fdcd3f10e1897e3d9548695b8cba98d8d44854856cc9c00c70eee41470dceb5; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3935931626; ctu=cb90e491e3f15f0564c9497c7f499eb83e80ad718d8ecbfa4da6e0b2b3f02407; uamo=15179833772; s_ViewType=10; wed_user_path=27811|0; aburl=1; cy=7; cye=shenzhen; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=165ac83ae18-6-41-db1%7C%7C29",
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
            shop_url_list.append(detal_url)
    else:
        print('请求异常，请确认响应地址[{}]'.format(page_url))


# 获取每个店铺的相关信息，进行数据处理，写入Excel
def get_detail(url):
    html = ''
    for i in range(3):
        html = requests.get(url, headers=headers).text
        if '验证中心' in html:
            print('需要输入验证码，请40秒内点击，然后重试。')
            time.sleep(10)
            continue
        else:
            break
    parse_detail(url, html)  # 传入需要解析的详情页面


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

# 获取评论
def get_comment(url, comment_url):
    global result
    headers['referer'] = url
    response = requests.get(comment_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews_list  = soup.find_all('div', class_='main-review')
    if len(reviews_list) == 0:
        return ''
    for reviews_ in reviews_list:
        name = reviews_.find('a', class_='name').get_text().replace('\n', '').strip()
        time = reviews_.find('span', class_='time').get_text().replace('\n', '').strip()
        review_words = reviews_.find('div', class_='review-words').get_text().replace('\n', '').strip()
        result += name + ' ' + time + ' ' + review_words + '\n'
    try:
        next_url = 'http://www.dianping.com' + soup.find('a', class_='NextPage')['href']
    except:
        next_url = 0
    if next_url:
        get_comment(url, next_url)
    return result


# 解析详情页面，写入Excel
def parse_detail(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        area = soup.find('div', class_='breadcrumb').get_text().replace('>', '»').replace(' ', '')
    except:
        area = '-'
    try:
        title = soup.find('h1', class_='shop-title').get_text()  # 门店名称
    except:
        title = '-'
    try:
        address = soup.find('span', itemprop='street-address').get_text()
    except:
        address = '-'
    try:
        comment_count = soup.find('ul', class_='cmt-filter').get_text()
    except:
        comment_count = 0
    try:
        status = soup.find('span', itemprop='rating').get_text().replace('\n', '').strip()
    except:
        status = 0
    comment_url = url + '/review_all'
    global result
    result = ''
    # print('拼发球', comment_count)
    # if comment_count != 0:
    comment_list = get_comment(url, comment_url)
    # else:
    #     comment_list = ''
    # try:
    #     phone = soup.find('p', class_='expand-info tel').get_text().replace('电话：', '').replace('添加', '')  # 电话
    # except:
    #     phone = ''
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
    print('采集到的数据为: ', area, title, address, comment_count, status, comment_list)
    sheet.append(['北京', '北京', area, title, address, comment_count, status, comment_list])


if __name__ == '__main__':
    sear_goods = ['yeehoo', '英氏', 'les', 'enphants']
    for goods in sear_goods:
        url = 'https://www.dianping.com/search/keyword/2/0_{}'.format(goods)
        get_shop_url(url)
    for shop_url in shop_url_list:
        get_detail(shop_url)
    book.save('大众点评-北京.xlsx')
    # get_detail('http://www.dianping.com/shop/66689745')
