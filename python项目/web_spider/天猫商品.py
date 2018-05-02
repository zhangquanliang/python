# -*- coding: utf-8 -*-
import re
import time
import datetime
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from fake_useragent import fake

from config import run_time, mysql_tools
# 初始化数据库连接
session, connect = mysql_tools()


# 传入任意一个想要输入的商品名字
def search(commodity):
    rq = requests.session()
    rq.get('https://www.tmall.com/')
    data = {
        "q": commodity
    }
    ua = fake.UserAgent()
    data = urlencode(data)
    create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 发送一个搜索请求
    url ='https://list.tmall.com/search_product.htm?{}&type=p'.format(data)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, sdch",
        "accept-language": "zh-CN,zh;q=0.8",
        "cache-control": "max-age=0",
        # "upgrade - insecure - requests": 1,
        "user-agent": ua.random
    }
    response = rq.get(url, headers=headers)
    response.encoding = 'gbk'
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    commodity_list = soup.find_all('div', class_='product-iWrap')
    print(len(commodity_list))
    # 增加多查询数据取前50条处理
    save_list = []
    for commodity_ in commodity_list:
        if len(save_list) == 50:
            break
        if 'productTitle' not in str(commodity_):
            continue
        try:
            commodity_img_url = "https:" + commodity_.find('img')['src']   # 图片地址
        except:
            commodity_img_url = "https:" + commodity_.find('img')['data-ks-lazyload']  # 图片地址
        if 'gif' in commodity_img_url:
            continue
        save_list.append(commodity_)
        try:
            commodity_price = re.findall('<b>.</b>(.*?)</em>', str(commodity_), re.I | re.S)[0]  # 商品金额
        except:
            commodity_price = "00000"
        try:
            commodity_name = commodity_.find('div', class_='productTitle productTitle-spu').find('a').get_text()   # 商品名
        except:
            commodity_name = commodity_.find('div', class_='productTitle ').find('a').get_text()
        commodity_shop = commodity_.find('a', class_='productShop-name').get_text().strip()   # 店铺名称
        try:
            commodity_pj = "月成交" + re.findall('<em>(.*?)笔</em>', str(commodity_))[0] + "笔"  # 商品成交量
        except:
            commodity_pj = "月成交" + "0" + "笔"
        try:
            commodity_url = "https:"+commodity_.find('div', class_='productTitle productTitle-spu').find('a')['href'].replace('amp;', '')  # 商品地址
        except:
            commodity_url = "https:" + commodity_.find('div', class_='productTitle ').find('a')['href'].replace('amp;', '')  # 商品地址
        if '笔记本' in commodity:
            sql = "insert into tm_bjb(commodity_name, commodity_price, commodity_url, commodity_pj," \
                  "commodity_shop, commodity_img_url, create_date) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                commodity_name, commodity_price, commodity_url, commodity_pj, commodity_shop, commodity_img_url, create_date)
        else:
            sql = "insert into tm_sj(commodity_name, commodity_price, commodity_url, commodity_pj," \
                  "commodity_shop, commodity_img_url, create_date) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                  commodity_name, commodity_price, commodity_url, commodity_pj, commodity_shop, commodity_img_url, create_date)
        session.execute(sql)
        connect.commit()


if __name__ == '__main__':
    print('天猫数据采集脚本运行中...')
    commodity_list = ['手机', '笔记本']
    while True:
        #  检验系统时间是否在设定运行时间中
        if run_time():
            for commodity in commodity_list:
                search(commodity)
            break
        else:
            print('本次校验结果: 运行时间不在设定运行时间中, 30秒后重新校验')
            time.sleep(30)
