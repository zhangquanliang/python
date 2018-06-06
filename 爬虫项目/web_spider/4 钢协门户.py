# -*- coding: utf-8 -*-
"""
Title = 中国钢协门户网
Date = 20180425
"""
import re
from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool


rq = requests.session()
headers = {
        "User-Agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*"
        }
m_url = 'http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&key=' \
             'CmlcYw1mWTgKa1NkUjUHZgZiBGcIbFJlBzQDMAJhATZWRQ1CDhUENgYXUhVUQwxs'


def mh_page():
    response = rq.get(m_url, headers=headers)
    reg = re.findall('共.*?条..1/(.*?)</a>', response.text)
    return int(reg[0])


def get_context(page):
    for i in range(page + 1):
        url = 'http://www.chinaisa.org.cn/gxportal/EiService'
        data = {
            "service": "ECTM02",
            "method": "turnPage",
            "eiinfo": "{attr: {'templateUnitInsId': '0000000000010086','nodeId': '0000000000000213', 'nodeType': 'c',  'currentPage': %d},"
                       "blocks: {}"
                      "}" % (i+1)
        }
        response = rq.post(url, data=data, headers=headers)
        pageString = response.json()['attr']['pageString']
        soup = BeautifulSoup(pageString, 'html.parser')
        result_list = soup.find_all('div', class_='subpage_inf_width')
        for result in result_list:
            href = "http://www.chinaisa.org.cn" + result.find('a')['href']
            title = result.find('a').get_text().replace('  ', '')   # 文章的标题
            date = result.find('span').get_text()     # 文章日期
            print(title, ">>>", date, ">>",  href)
            print('-' * 100)

            # response = rq.get(href, headers=headers)
            # reg = re.findall('iframe id="mframe" src="(.*?)" frameborder=', response.text)
            # url = "http://www.chinaisa.org.cn" + reg[0]   # 文章的具体地址
            # response = rq.get(url, headers=headers)
            # response.encoding = 'gbk'
            # parser_html(title, response.text)


# 解析文章具体内容
def parser_html(title, html):
    context = ""
    soup = BeautifulSoup(html, 'html.parser')
    result_list = soup.find_all('p', class_='MsoNormal')
    for result_ in result_list:
        result = result_.find_all('span')
        for rs in result:
            context += rs.get_text()
    print(title, " >>> " + context)
    print('-' * 70)


def start_pool():
    page = mh_page()
    pool = Pool(processes=20)
    pool.apply_async(get_context, [page])
    pool.close()
    pool.join()


if __name__ == '__main__':
    start_pool()