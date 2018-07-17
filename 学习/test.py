# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

drive = webdriver.Ie(executable_path=r'D:\C Git\D project\zhangql\util_zql\IEDriverServer(zql).exe')
drive.maximize_window()
drive.get('https://www.baidu.com')

drive.set_script_timeout(12)
drive.find_element_by_id("su").click()
drive.quit()