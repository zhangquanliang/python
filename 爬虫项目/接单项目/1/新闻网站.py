# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
import random
import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
ip_list = [
    "https://180.105.233.87:3797",  # 180.105.233.87 为IP 3797为端口
    "https://114.237.52.225:4260",
    "https://114.237.50.50:4149",
    "https://112.252.70.124:4073",
    "https://114.228.213.178:4678",
    "https://117.63.52.147:9817",
    "https://115.221.12.187:6249 ",
    "https://121.232.39.183:6015",
    "https://115.228.198.61:9865",
    "https://39.81.149.229:9997"
]
ua = FakeUserAgent()


def get_html(page):
    user_agent = ua.random
    headers = {
        "User-Agent": user_agent
    }
    url = 'https://search.archives.gov/search?affiliate=obamawhitehouse&op=Search&page={}&query=STEM'.format(page)
    ip = {
        "https": random.choice(ip_list)
    }
    response = requests.get(url, proxies=ip, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    url_list_ = soup.find_all('span', class_='url')
    for url_ in url_list_:
        t_url = url_.get_text()
        if 'video' in t_url:
            continue
        print('url', t_url)
        resp = requests.get(t_url, proxies=ip, headers=headers)
        parse_html(resp.text)
        time.sleep(2)


def parse_html(html):
    if 'panel-pane pane-node-title' and 'content' not in html:
        return
    soup = BeautifulSoup(html, 'html.parser')

    if 'panel-pane pane-node-title' in html:
        title = soup.find('div', class_='panel-pane pane-node-title').get_text().strip()
        context = soup.find('div', class_='panel-panel panel-col panel-col-section-content-third').get_text().replace('\\n', '')
    elif 'content' or 'webform-description' in html:
        title = soup.find('div', id='content').find('h1').get_text()
        context = soup.find('div', class_='webform-description').get_text().replace('\\n', '')
    else:
        title = "1"
        context = "1"
    title = title.replace('?', '').replace('!', '').replace(':', '').replace('#', '')
    file = './wenzhang/' + title + '.txt'
    with open(file, 'a+', encoding='utf8') as f:
        f.write(context)
        f.flush()


if __name__ == '__main__':
    pool = Pool(processes=20)
    for i in range(1, 105):
        pool.apply_async(get_html, [i])
        # break
    pool.close()
    pool.join()