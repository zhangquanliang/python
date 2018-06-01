# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
import datetime
import requests
import pymysql
pymysql.install_as_MySQLdb()

from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from bs4 import BeautifulSoup

req = requests.session()   # 保持请求头部信息

url = 'http://jb39.com/zhengzhuang/zhengzhuang-all.htm'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "jb39.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
}


# 主函数
def get_symptom_url():
    symptom_url_list = []
    res = req.get(url, headers=headers)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, 'html.parser')
    ul_list = soup.find_all('ul', class_='post-mulu')[0]
    for li in ul_list.find_all('li'):
        symptom_url = 'http://jb39.com' + li.find('a')['href']
        symptom_url_list.append(symptom_url)
    return symptom_url_list


# 入口函数
def get_symptom_context(url):
    response = req.get(url, headers=headers)
    response.encoding = 'gbk'
    parser_html(response.text)


# 解析入口函数返回的数据包
def parser_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    mingchen = soup.find('h2', class_='h2-gr jb-search').get_text()    # 名称
    bieming = soup.find('span', class_='spider').get_text()   # 别名
    jianjie = soup.find('p', class_='zz-body').get_text()     # 简介
    bingyin_url = 'http://jb39.com' + soup.find('h2', class_='jb-h2 zz-by-index').find('a')['href']    # 病因全部地址
    jiancha_url = 'http://jb39.com' + soup.find('h2', class_='jb-h2 zz-jc-index').find('a')['href']  # 检查全部地址
    zhenduan_url = 'http://jb39.com' + soup.find('h2', class_='jb-h2 zz-zd-index').find('a')['href']  # 诊断全部地址
    bingyin = parser_more(bingyin_url)
    jiancha = parser_more(jiancha_url)
    zhenduan = parser_more(zhenduan_url)

    buwei_list = soup.find('ul', class_='ul-ss-3 zz-xx-bw').find_all('li')  # 症状部位
    buwei = get_zz(buwei_list)
    keshi_list = soup.find('ul', class_='ul-ss-3 zz-xx-ks').find_all('li')  # 症状科室
    keshi = get_zz(keshi_list)
    zhengzhuan_list = soup.find('ul', class_='ul-ss-3 zz-xx-zz').find_all('li')  # 相关症状
    zhengzhuan = get_zz(zhengzhuan_list)
    jibing_list = soup.find('ul', class_='ul-ss-3 zz-xx-jb').find_all('li')  # 相关疾病
    jibing = get_zz(jibing_list)
    zzjiancha_list = soup.find('ul', class_='ul-ss-3 zz-xx-jc').find_all('li')  # 症状检查
    zzjiancha = get_zz(zzjiancha_list)
    create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if '男' in jianjie or '男' in bingyin or '男' in jiancha:
        xiangguanrq = '男人'
    elif '女' in jianjie or '女' in bingyin or '女' in jiancha:
        xiangguanrq = '女人'
    else:
        xiangguanrq = '所有人群'

    sql = "insert into zzdq(mingchen, bieming, jianjie, bingyin, jiancha, zhenduan, buwei, keshi, zhengzhuan," \
          " jibing, zzjiancha, xiangguanrq,create_date) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')" \
        .format(mingchen, bieming, jianjie, bingyin, jiancha, zhenduan, buwei, keshi, zhengzhuan, jibing, zzjiancha,
                xiangguanrq, create_date)
    try:
        db_insert(sql)
        print('症状[{}], 别名[{}], 入库成功！' .format(mingchen, bieming))
    except Exception as ex:
        print('入库异常! {}'.format(ex))


def get_zz(zz_list):
    if len(zz_list) == 1:
        return zz_list[0].find('a').get_text()
    result = ""
    for i in zz_list:
        s = i.find('a').get_text()
        result += s + "$"
    return result[:-1]


# 数据库连接入库
def db_insert(sql):
    conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='dianshang', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# 对病因, 检查，诊断数据数据采集全部做处理
def parser_more(url):
    rs = req.get(url, headers=headers)
    rs.encoding = 'gbk'
    bysoup = BeautifulSoup(rs.text, 'html.parser')
    result = bysoup.find('div', class_='spider').get_text().strip()
    time.sleep(1)
    return result


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=10)
    all_task = []
    for symptom_url in get_symptom_url():
        fu = pool.submit(get_symptom_context, symptom_url)
        all_task.append(fu)
        # break
    wait(all_task)
    # session.close()
    # connect.close()
