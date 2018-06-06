# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
import requests
import urllib3
urllib3.disable_warnings()
from selenium import webdriver


class ZhiHu:
    def __init__(self):
        self.url = 'https://www.zhihu.com/'
        self.headers = {
            "User-Agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "cache-control": "max-age=0"
        }

    # 登录
    def login(self):
        url = 'https://www.zhihu.com/signup?next=%2F'
        driver = webdriver.PhantomJS(executable_path=r'D:\C Git\D project\zhangql\util_zql\phantomjs.exe')
        driver.get(url)
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
            time.sleep(0.6)
            driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys('15179833772')
            time.sleep(0.6)
            driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys('ZQL131415')
            time.sleep(0.6)
            driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
        except:
            pass
        time.sleep(5)
        if '热门内容' in driver.page_source:
            cookies = driver.get_cookies()
            cookie = ""
            for cookie_ in cookies:
                cookie = "%s=%s;%s" % (cookie_["name"], cookie_["value"], cookie)
            self.headers['Cookie'] = cookie.replace('"', '')
        else:
            driver.quit()
            return self.login()

    # 校验Cookie是否失效
    def check_login(self, html=None):
        if html is None:
            url = 'https://www.zhihu.com/'
            response = requests.get(url, headers=self.headers, verify=False)
            return False if '验证码' in response.text and response.status_code == 200 else True
        else:
            return False if '验证码' in html else True

    # 获取live用户关注的live信息
    def get_live(self):
        if not self.check_login():
            self.login()
        self.get_users()

    # 获取到所有用户
    def get_users(self):
        self.headers["referer"] = "https://www.zhihu.com/people/zhangql_zh/activities"
        response = requests.get(self.url, headers=self.headers, verify=False)
        print(response.url)
        print(response.text)


if __name__ == '__main__':
    zh = ZhiHu()
    zh.get_live()