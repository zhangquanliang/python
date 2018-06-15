# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Ie(executable_path=r'D:\C Git\D project\zhangql\util_zql\IEDriverServer(zql).exe')
driver.get('https://www.che168.com/china/list/')
driver.find_element_by_xpath('//*[@id="brandmore"]').click()
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
brand_list = soup.find_all('div', class_='brand2-city')
csvFile = open('车系.csv',  'w', newline='', encoding='utf8')
writer = csv.writer(csvFile)
writer.writerow(['车系', '车系地址'])
for brand_ in brand_list:
    for brand in brand_.find_all('a'):
        car_dict = {}
        brand_href = 'https://www.che168.com' + brand['href'].strip()
        driver.get(brand_href)
        if 'hotseriesmore' not in driver.page_source:
            soup3 = BeautifulSoup(driver.page_source, 'html.parser')
            con_mini_list = soup3.find('div', class_='second-list condition-list fn-clear').find_all('a', class_='con-mini')
            for con_mini_ in con_mini_list:
                con_mini_url = 'https://www.che168.com' + con_mini_['href']
                con_mini_name = con_mini_.get_text().strip()
                car_dict[con_mini_name] = con_mini_url
            continue
        driver.find_element_by_xpath('//*[@id="hotseriesmore"]').click()
        time.sleep(2)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        con_mini_list = soup2.find('div', class_='condition-list fn-clear fn-hide').find_all('a', class_='con-mini ')
        for con_mini_ in con_mini_list:
            con_mini_url = 'https://www.che168.com' + con_mini_['href']
            con_mini_name = con_mini_.get_text().strip()
            car_dict[con_mini_name] = con_mini_url
        for k, v in car_dict.items():
            writer.writerow([k, v])
    # break