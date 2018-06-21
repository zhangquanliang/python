# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
from selenium import webdriver


def get_cookie(login_user, login_password):
    # writer2.writerow([login_user, login_password])
    url = 'https://login.aliexpress.com/buyer.htm'
    driver = webdriver.Chrome(executable_path=r'D:\C Git\D project\zhangql\util_zql\chromedriver(zql).exe')
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)
    driver.switch_to.frame('alibaba-login-box')
    driver.find_element_by_id('fm-login-id').clear()
    driver.find_element_by_id('fm-login-id').send_keys(login_user)
    time.sleep(1)
    driver.find_element_by_id('fm-login-password').clear()
    driver.find_element_by_id('fm-login-password').send_keys(login_password)
    time.sleep(1)
    driver.find_element_by_id('fm-login-submit').click()
    time.sleep(20)
    # driver.implicitly_wait(30)
    cookies = driver.get_cookies()
    cookie = ""
    for cookie_ in cookies:
        cookie = "%s;%s=%s" % (cookie, cookie_["name"], cookie_["value"])
    driver.quit()
    f = r'cookies\{}.txt'.format(login_user)
    with open(f, 'w', encoding='utf-8') as f:
        f.write(cookie)
        f.flush()
    return cookie


if __name__ == '__main__':
    login_dict = [
        # {'login_user': '9711@nbchina.win', 'login_password': 'h70351'},
        {'login_user': '9712@nbchina.win', 'login_password': 'x41355'},
        {'login_user': '9713@nbchina.win', 'login_password': 'f17298'},
        {'login_user': '9714@nbchina.win', 'login_password': 'a77940'},
        # {'login_user': '9715@nbchina.win', 'login_password': 'q20640'},
        # {'login_user': '9716@nbchina.win', 'login_password': 'b92412'},
        # {'login_user': '9717@nbchina.win', 'login_password': 'e62369'},否
        # {'login_user': '9718@nbchina.win', 'login_password': 'Y69314'}, 否
        # {'login_user': '9719@nbchina.win', 'login_password': 'X13639'}, 否
        # {'login_user': '9720@nbchina.win', 'login_password': 'd74310'}
        ]
    for j in reversed(login_dict):
        cookie = get_cookie(j['login_user'], j['login_password'])
        print(cookie)
        time.sleep(60)