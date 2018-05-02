# -*- coding: utf-8 -*-
import re
import time
import datetime

import requests
from bs4 import BeautifulSoup

from config import run_time, mysql_tools
# 初始化数据库连接
session, connect = mysql_tools()


# 传入任意一个想要输入的商品名字
def search(commodity):
    rq = requests.session()
    create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url ='https://search.suning.com/{}/'.format(commodity)
    # 发送一个搜索请求
    response = rq.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    commodity_list = soup.find_all('div', class_='product-box')

    # 增加多查询数据取前50条处理
    save_list = []
    for commodity_ in commodity_list:
        print()
        if len(save_list) == 50:
            break
        commodity_img_url = "https:" + commodity_.find('img')['src2']   # 图片地址
        commodity_name = commodity_.find('a', class_='sellPoint')['title']  # 商品名
        commodity_url = "https:" + commodity_.find('a', class_='sellPoint')['href']  # 商品地址
        save_list.append(commodity_)

        reg = re.findall("addToInterests\('.*?','(.*?)',this\)", str(commodity_))[0]
        price_url = 'https://ds.suning.cn/ds/generalForTile/{}_,-752-2-0000000000-1--ds0000000006206.jsonp'.format(reg)
        price_response = rq.get(price_url)
        commodity_price = re.findall('"cmmdtyCode":"{}","price":"(.*?)",'.format(reg), str(price_response.text), re.I | re.S)[0]  # 商品金额
        res = rq.get(commodity_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        commodity_shop = soup.find('div', class_='si-intro-list').find('a', target='_blank')  # 店铺名称
        if commodity_shop is None:
            commodity_shop = ""
        else:
            commodity_shop = commodity_shop.get_text()
        if '笔记本' in commodity or '游戏本' in commodity_name:
            sql = "insert into sn_bjb(commodity_name, commodity_price, commodity_url," \
                  "commodity_shop, commodity_img_url, create_date) values('%s', '%s', '%s', '%s', '%s', '%s')" % (
                      commodity_name, commodity_price, commodity_url, commodity_shop, commodity_img_url, create_date)
        else:
            sql = "insert into sn_sj(commodity_name, commodity_price, commodity_url," \
                  "commodity_shop, commodity_img_url, create_date) values('%s', '%s', '%s', '%s', '%s', '%s')" % (
                      commodity_name, commodity_price, commodity_url, commodity_shop, commodity_img_url, create_date)
        session.execute(sql)
        connect.commit()


if __name__ == '__main__':
    print('苏宁数据采集脚本运行中...')
    commodity_list = ['笔记本', '手机']
    while True:
        #  检验系统时间是否在设定运行时间中
        if 1:
            for commodity in commodity_list:
                search(commodity)
            break
        else:
            print('本次校验结果: 运行时间不在设定运行时间中, 30秒后重新校验')
            time.sleep(30)
