# -*- coding: utf-8 -*-
import urllib.parse
from selenium import webdriver
import urllib.request

# driver = webdriver.PhantomJS(executable_path=r'D:\Git\MyProject\zhangql\resources\phantomjs.exe')
# driver.get('http://www.baidu.com')
#
# print(driver.current_url)
response = urllib.request.urlopen('http://www.baidu.com')
print(response.read().decode('utf-8'))