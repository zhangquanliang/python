# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    movie_name = input('请输入想要下载的电影: ')
    url = 'http://so.iqiyi.com/so/q_%s' % movie_name
    html = requests.get(url=url).text
    soup = BeautifulSoup(html, 'html.parser')
    a = re.search(r'<a class="figure\s\sfigure-.*\s?', html).group()
    b = (a.split("-")[1])
    c = str(b).split(' "')[0]

    movie_ = soup.find('li', class_='list_item')
    class_f = 'figure figure-%s ' % c
    movie_url = movie_.find('a', class_=class_f).get('href')
    print(u'你想要下载的电影为 %s' % movie_name)
    print(u'电影地址是: %s' % movie_url)
    urls = 'http://api.xfsub.com/index.php?url=%s' % movie_url
    print(urls)
    ca =requests.get(urls).text
    print(ca)
