# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
import requests
import random
import datetime
from multiprocessing.dummy import Pool      # 导入多线程模块
from selenium import webdriver
from config_d import mysql_tools, headers_list   # 从配置文件中导入数据库连接，ua代理池


# 1 登陆功能
def login():
    driver = webdriver.Ie(executable_path=r'D:\C Git\D project\zhangql\util_zql\IEDriverServer(zql).exe')
    login_url = 'https://www.douban.com/accounts/login?source=movie'
    driver.get(login_url)
    # 随机等待0-1秒
    time.sleep(random.random())

    # 清空用户名输入框，并输入自己的账号
    driver.find_element_by_id('email').clear()
    driver.find_element_by_id('email').send_keys('15179833772')      # 用户名
    time.sleep(0.5)

    # 清空密码输入框，并输入自己的密码
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys('ZQL131415..')    # 密码
    time.sleep(0.5)

    # 点击登陆按钮，实现登陆功能
    driver.find_element_by_class_name('btn-submit').click()   # 登陆
    # 随机等待2-5秒
    time.sleep(random.randint(2, 5))
    # 判断网页地址是否跳转，跳转代表登陆成功，否则失败
    if login_url != driver.current_url:
        print('222222')
        driver.get('https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0')
        time.sleep(0.5)
        cookies = driver.get_cookies()
        cookie = ""
        for cookie_ in cookies:
            cookie = "%s;%s=%s" % (cookie, cookie_["name"], cookie_["value"])
        print('登陆成功..')
        driver.quit()
        return True, cookie
    else:
        print('登陆失败, 重新登陆！')
        driver.quit()
        return False, ''


# 开启线程
def start_process():
    # 创建10个线程的线程池
    pool = Pool(processes=10)
    # 采集豆瓣热门电影的前16页数据。每页20条
    for i in range(16):
        # 线程异步请求
        pool.apply_async(get_movies, [i])
        # break
    pool.close()
    pool.join()


# 获取电影的信息
def get_movies(i):
    page_start = i * 20
    url = 'https://movie.douban.com/j/search_subjects?type=movie' \
          '&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}'.format(page_start)
    # 从用户代理池中随机抽取一个ua，实现反反爬
    user_agent = random.choice(headers_list)
    headers = {
        "User-Agent": user_agent,
        "Referer": "https://movie.douban.com/explore"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print('请求异常, 确认地址!返回地址为:{}'.format(res.url))
    else:
        # 解析响应的json数据
        parse_json(res.json())
    # 随机等待2-5秒
    time.sleep(random.randint(2, 5))


# 2 解析返回的数据
def parse_json(json_str):
    # 初始化数据库连接
    session, connect = mysql_tools()
    movie_list = json_str['subjects']
    for movie in movie_list:
        m_name = movie['title']
        rate = movie['rate']
        url = movie['url']
        is_new = movie['is_new']
        image_url = movie['cover']
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('电影名[%s], 评分[%s], 电影详情地址[%s], 是否最新[%s], 电影图片地址[%s]' % (m_name, rate, url, is_new, image_url))
        sql = "insert into douban_movie(m_name, rate, url, is_new, image_url, create_date)" \
              " values ('{}', '{}', '{}', '{}', '{}', '{}')".format(m_name, rate, url, is_new, image_url, create_date)
        session.execute(sql)    # 执行sql，实现数据库存储
        connect.commit()
    # 数据库连接关闭
    session.close()
    connect.close()


if __name__ == '__main__':
    # issuccess, cookie = login()
    # if issuccess:   # 登陆接口，如需要登陆，取消注释，去修改里面的用户名，密码即可
    if 1:     # 不需要登陆，就直接改成if 1，同样可以采集数据。
        start_process()
    else:
        print('登录失败...')
