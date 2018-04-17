# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
class TaoBao:
    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path=r'D:\C Git\D project\zhangql\util_zql\phantomjs.exe')

    # 商品
    def commodity(self, commodity):
        search_url = 'https://qiang.taobao.com/?spm=a21bo.2017.2003.1.1dcd11d9BBewXJ'
        self.driver.get(search_url)

        print(self.driver.page_source)


if __name__ == '__main__':
    taobao = TaoBao()
    commodity = '男鞋'
    taobao.commodity(commodity=commodity)