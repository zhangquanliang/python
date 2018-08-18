# -*- coding: utf-8 -*-
import re
import time
import datetime
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

from config import run_time, mysql_tools
# 初始化数据库连接
session, connect = mysql_tools()


# 传入任意一个想要输入的商品名字
def search(commodity):
    rq = requests.session()
    create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "keyword": commodity
    }
    commodity = urlencode(data)

    # 发送一个搜索请求
    url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format(commodity)
    rq.get(url)
    headers = {
        "referer": url,
        "user-agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    save_list = []  # 增加多查询数据取前50条处理
    for i in range(2):
        url = 'https://search.jd.com/s_new.php?keyword={}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={}&s=27&scrolling=y'.format(commodity, i+1)
        response = rq.get(url, headers=headers)

        # 将返回的结果传入parser_html函数中解析
        parser_html(response.text, save_list, create_date)


# 解析返回的页面，提取所需要的数据
def parser_html(html, save_list, create_date):
    soup = BeautifulSoup(html, 'html.parser')
    commodity_list = soup.find_all('li', class_='gl-item')

    for commodity_ in commodity_list:
        if len(save_list) == 50:
            break
        try:
            commodity_img_url = "http:" + commodity_.find('img')['src']  # 图片地址
        except:
            commodity_img_url = "http:" + commodity_.find('img')['data-lazy-img']  # 图片地址
        save_list.append(commodity_)
        commodity_price = commodity_.find('div', class_='p-price').get_text().strip().replace('￥', '')  # 商品金额
        if commodity_price == '' or commodity_price is None:
            commodity_price = commodity_.find('strong')['data-price']  # 商品金额
        commodity_name = commodity_.find('div', class_='p-name p-name-type-2').get_text().strip()  # 商品名
        commodity_shop = commodity_.find('div', class_='p-shop').get_text().strip()  # 店铺名称
        commodity_pj = re.findall('target="_blank">(.*?)</a>条评价', str(commodity_))[0]  # 商品评价数量
        commodity_url = commodity_.find('a', target="_blank")['href']  # 商品地址
        if 'https' not in commodity_url:
            commodity_url = "http:" + commodity_url
        # print(commodity_name, commodity_price, commodity_url, commodity_pj,commodity_shop, commodity_img_url)
        # print('-' * 100)
        if '笔记本' in commodity_name:
            sql = "insert into jd_bjb(commodity_name, commodity_price, commodity_url, commodity_pj," \
                  "commodity_shop, commodity_img_url, create_date) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                commodity_name, commodity_price, commodity_url, commodity_pj, commodity_shop, commodity_img_url, create_date)
        else:
            sql = "insert into jd_sj(commodity_name, commodity_price, commodity_url, commodity_pj," \
                  "commodity_shop, commodity_img_url, create_date) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                  commodity_name, commodity_price, commodity_url, commodity_pj, commodity_shop, commodity_img_url, create_date)
        session.execute(sql)
        connect.commit()


if __name__ == '__main__':
    print('京东数据采集脚本运行中...')
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
