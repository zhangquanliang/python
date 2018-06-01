# python3.6.3
# coding: utf-8
# @Time    : 5/28/20118
# @Author  : 张思宇
# @email   : 1234567890@163.com
# @Site    :
# @File    : news
# @Software: PyCharm
# 导入所需要的模块
from lxml import etree
import requests
import time
import re
from bs4 import BeautifulSoup
import random
from multiprocessing.dummy import Pool
import json

# 模仿用户的行为
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    '39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/'
    '23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/'
    '10.0.648.133 Safari/534.16',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5", ]
# 伪装成浏览器的头
headers = {
    "User-Agent": random.choice(user_agent_list)
}


# 获取所有的地址
def get_all_url():
    base_url = 'http://news.people.com.cn/210801/211150/index.js?_=1527517323681'
    # 获取接口的网页源码，并且使用动态代理
    response = requests.get(url=base_url,
                            proxies={'http': 'http://H01T3Z8ZSM11D61D:154F545DD00DA6B3@proxy.abuyun.com:9020',
                                     'https': 'http://H01T3Z8ZSM11D61D:154F545DD00DA6B3@proxy.abuyun.com:9020'},
                            headers=headers).text
    result = []
    data = json.loads(response)
    detail_links = data['items']
    for detail_link in detail_links:
        url = detail_link['url']
        result.append(url)
    return result


# 获取每个文章的数据
def parse_html(url):
    print(url)
    source_code = requests.get(url=url,
                               proxies={'http': 'http://H01T3Z8ZSM11D61D:154F545DD00DA6B3@proxy.abuyun.com:9020',
                                        'https': 'http://H01T3Z8ZSM11D61D:154F545DD00DA6B3@proxy.abuyun.com:9020'},
                               headers=headers)
    # 自动转换编码格式
    source_code.encoding = source_code.apparent_encoding
    detali_code = source_code.text
    soup = BeautifulSoup(detali_code, 'lxml')
    contents = soup.find_all("div", class_="box_con")
    for content in contents:
        print(content.text)


if __name__ == '__main__':
    url_list = get_all_url()
    pool = Pool(processes=10)
    for url in url_list:
        pool.apply_async(parse_html, [url])
    pool.close()
    pool.join()