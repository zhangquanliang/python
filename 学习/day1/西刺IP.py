# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
import requests
req = requests.session()
from multiprocessing.dummy import Pool
from fake_useragent import FakeUserAgent
ua = FakeUserAgent()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Host": "www.xicidaili.com",
    "Referer": "http://www.xicidaili.com/nn/",
    "User-Agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
}


def all_ip():
    pool = Pool(processes=10)
    for i in range(1, 1001):
        url = 'http://www.xicidaili.com/nn/{}'.format(i)
        try:
            user_agent = ua.random
            headers['User-Agent'] = user_agent
            response = req.get(url, headers=headers)
            pool.apply_async(parse_html, [response.text])
        except:
            continue
    pool.close()
    pool.join()


def parse_html(html):
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    ip_table = soup.find('table', id='ip_list')
    for ip_tr in ip_table.find_all('tr'):
        ip_td = ip_tr.find_all('td')
        if len(ip_td) == 0:
            continue
        ip = ip_td[1].get_text()  # ip地址
        port = ip_td[2].get_text()   # 端口
        # type = ip_td[1].get_text()
        check_proxies(ip, port)


def check_proxies(ip, port):
    # url = 'http://pv.sohu.com/cityjson?ie=utf-8'
    url = 'http://www.baidu.com'
    proxies = {'http': 'http://{}:{}'.format(ip, port)}
    print(proxies)
    try:
        response = req.get(url, proxies=proxies, headers=headers, timeout=5)
        if response.status_code == 200 and '百度搜索' in response.text:
            print('success', ip, port)
            with open('有效IP', 'a+', encoding='utf-8') as f:
                f.write(ip + " " * 3 + port + '\n')
    except Exception as ex:
        pass


all_ip()

