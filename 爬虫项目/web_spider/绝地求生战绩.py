# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
from selenium import webdriver
from bs4 import BeautifulSoup


def get_user_zhanji(user_name):
    url = 'http://pubg.ali213.net/pubg10/overview?nickname={}&f='.format(user_name)
    driver = webdriver.PhantomJS(executable_path=r'D:\C Git\D project\zhangql\util_zql\phantomjs.exe')
    driver.get(url)
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[3]/div[1]/div/div[2]/div[2]/li[1]/div[1]').click()
    time.sleep(0.5)

    html = driver.page_source
    parse_html(html)
    driver.quit()


# 解析得到的数据
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    new_zhangji = soup.find('div', class_='leftDetials-cont match-info')
    ul = new_zhangji.find('ul', class_='flex-box vertical')
    li_list = ul.find_all('li')
    result = {}
    for i in li_list:
        key = i.find('div', class_='k').get_text().strip().replace('&nbsp;', '')
        value = i.find('div', class_='v').get_text().strip()
        result[value] = key
    chijicishu = soup.find('div', class_='chengjiu-item-l').find('div', class_='con').get_text().strip()
    qianshicishu = soup.find('div', class_='chengjiu-item-r').find('div', class_='con').get_text().strip()
    result['吃鸡次数'] = chijicishu
    result['前十次数'] = qianshicishu
    print(result)


if __name__ == '__main__':
    user_name = 'ChristmasDK'
    get_user_zhanji(user_name)