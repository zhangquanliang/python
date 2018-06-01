# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from bs4 import BeautifulSoup


# 填写用户名密码
def login(login_user, login_password):
    for i in range(3):
        driver = webdriver.Ie(executable_path=r'D:\C Git\D project\zhangql\util_zql\IEDriverServer(zql).exe')
        url = 'http://ypz.youmaijinkong.com/m/home/enter?weauth=false'
        driver.get(url)
        time.sleep(1)
        driver.find_element_by_id('CellPhoneNumber').send_keys(login_user)
        time.sleep(1)
        driver.find_element_by_id('Password').send_keys(login_password)
        time.sleep(60)
        driver.find_element_by_xpath('//*[@id="formSignin"]/button').click()
        try:
            time.sleep(5)
            # 捕获错误信息
            error = driver.find_element_by_xpath('//DIV[@class="weui-dialog__bd"]').text
            print(error)
            driver.quit()
            continue
        except:
            pass

        if '未注册' in driver.page_source:
            driver.refresh()
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div[4]/a[2]/img').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="divTabs"]/div[1]/span').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="divTabs"]/div[2]/div[2]/label[1]').click()
            time.sleep(1)
            parse_html(driver.page_source)
            driver.quit()
            break
        except:
            driver.quit()
            continue


# 解析得到得数据
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    datalist = soup.find('div', id='datalist')
    for i in datalist.find_all('a', class_='card-container'):
        mingzi = i.find('div', class_='ml10 text-center').get_text()   # 人名
        jiekuan = i.find('div', class_='weui-flex__item text-right').get_text()    # 金额
        yongtu = i.find_all('div', class_='weui-flex border-bottom')[1].get_text()  # 用途
        zhuangtai = i.find_all('div', class_='text-right')[1].get_text()    # 状态
        print(mingzi, ' ', jiekuan, ' ', yongtu, ' ', zhuangtai)


if __name__ == '__main__':
    login_user = '17786506171'
    login_password = '147258'
    login(login_user, login_password)