# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import datetime
import pymysql
import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
house_dict = {}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/65.0.3325.181 Safari/537.36",
    "Host": "www.517.cn"
}


# 数据库连接入库
def db_insert(house_id, sql):
    conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='spider_j', charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        print('保存房源编号为: {}成功...'.format(house_id))
    except:
        print('保存房源编号为: {}失败!!!'.format(house_id))
    finally:
        cursor.close()
        conn.close()


# test_url = 'http://www.517.cn/ershoufang/2664185/'
def parse_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    area = soup.find('div', class_='path-nav').find_all('a')[2].get_text().replace('二手房', '')    # 沈河区
    address = soup.find('div', class_='path-nav').find_all('a')[3].get_text().replace('二手房', '')     # 丰乐
    title = soup.find('span', id='ContentPlaceHolder1__labTitle').get_text()   # 溪林花园两室两厅，位置好交通方便
    house_id = soup.find('div', id='ContentPlaceHolder1__pHouseTags').find('i').get_text().replace('房源编号：', '') # 2664185
    try:
        read_number = soup.find('label', id='lblLiuLan').get_text()   # 10
    except:
        read_number = 0
    price = soup.find('div', class_='shoujia clearfix').find_all('li')[0].get_text()   # 72万
    house_type = soup.find('div', class_='shoujia clearfix').find_all('li')[1].get_text()   # 2室2厅1卫
    floor_space = soup.find('div', class_='shoujia clearfix').find_all('li')[2].get_text()   # 120m2
    try:
        floor = soup.find('div', class_='o-info clearfix').find_all('li')[1].get_text().replace('楼层：', '')   # 楼层：高层（共7层）
    except:
        floor = ''
    try:
        orientation = soup.find('div', class_='o-info clearfix').find_all('li')[2].get_text().replace('朝向：', '')  # 朝向：南北
    except:
        orientation = ''
    try:
        decoration = soup.find('div', class_='o-info clearfix').find_all('li')[3].get_text().replace('装修：', '')  # 装修：老式装修
    except:
        decoration = ''
    try:
        house_age = soup.find('div', class_='o-info clearfix').find_all('li')[4].get_text().replace('房龄：', '')  # 房龄：1998年
    except:
        house_age = ''
    try:
        house_community = soup.find('div', class_='o-info clearfix').find_all('li')[6].find_all('a')[0].get_text()  # 溪林花园
    except:
        house_community = ''
    localhost = soup.find('div', class_='o-info clearfix').find_all('li')[7].find('a')[0].get_text() # 沈阳市沈河区文萃路179-16号
    name = soup.find('li', class_='m-jjr-name').get_text()  # 张新闯
    try:
        level = soup.find('div', class_='j-lv-tishi').get_text()  # D9
    except:
        level = ''
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if house_id == house_dict['house_id']:
        return
    else:
        sql = "insert into mangguo_esf values (" \
              " '{}', '{}', '{}', '{}', '{}'," \
              " '{}', '{}', '{}', '{}','{}'," \
              " '{}', '{}', '{}', '{}', '{}'," \
              " '{}', '{}')".format(
                area, address, title, house_id, read_number,
                price, house_type, floor_space, floor, orientation,
                decoration, house_age, house_community, localhost, name,
                level, create_time)
        db_insert(house_id, sql)
        house_dict['house_id'] = house_id


def get_house_details(detail_url):
    response = requests.get(detail_url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200 and response.url == detail_url:
        parse_detail(response.text)
    else:
        print('进入详情页面异常，响应地址! {}'.format(response.url))


def get_house(i):
    url = 'http://www.517.cn/ershoufang/pgq1?ckattempt=1/pg{}/'.format(i)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    if res.status_code == 200 and res.url == url:
        soup = BeautifulSoup(res.text, 'html.parser')
        house_list = soup.find_all('div', class_='ListBox-I clearfix')
        for house_ in house_list:
            try:
                detail_url = 'http://www.517.cn' + house_.find('div', class_='details').find('h3').find('a')['href']
                get_house_details(detail_url)
            except Exception as ex:
                print('获取房子详情地址异常，异常原因【{}】'.format(ex))
                return
    else:
        print('查询房屋信息异常，异常地址为：{}'.format(url))


def start_pool():
    pool = Pool(processes=10)
    for i in range(1, 3358):
        pool.apply_async(get_house, [i])
        break
    pool.close()
    pool.join()


if __name__ == '__main__':
    start_pool()