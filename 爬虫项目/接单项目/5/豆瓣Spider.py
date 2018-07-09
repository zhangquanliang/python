# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time
import requests
import random
import datetime
from multiprocessing.dummy import Pool      # 导入多线程模块
from config_d import mysql_tools, headers_list   # 从配置文件中导入数据库连接，ua代理池


# 1 登陆功能
def login():
    req = requests.session()
    login_url = 'https://www.douban.com/accounts/login?source=movie'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    req.get(login_url, headers=headers)
    data = {
        "source": "movie",
        "redir": "https://www.douban.com",
        "form_email": "15179833772",   # 改成自己的账号
        "form_password": "ZQL131415..",  # 改成自己的密码
        "login": "登录"
    }
    post_url = 'https://accounts.douban.com/login'
    headers['Referer'] = login_url
    res = req.post(post_url, headers=headers, data=data)
    if res.status_code == 200 and '我的钱包' in res.text:
        cookie = ''
        for k, v in req.cookies.items():
            cookie += ';{}={}'.format(k, v)
        print('登陆成功, 获取到的cookie为: ', cookie)
        return cookie
    else:
        print(res.url)
        if 'Please try later' in res.text:
            print('登陆频繁, 请稍后重试! ')
        else:
            print('登陆失败')
        return False


# 开启线程
def start_process(cookie):
    # 创建10个线程的线程池
    pool = Pool(processes=10)
    # 采集豆瓣热门电影的前16页数据。每页20条
    for i in range(16):
        # 线程异步请求
        pool.apply_async(get_movies, (i, cookie))
        # break
    pool.close()
    pool.join()


# 获取电影的信息
def get_movies(i, cookie):
    page_start = i * 20
    url = 'https://movie.douban.com/j/search_subjects?type=movie' \
          '&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}'.format(page_start)
    # 从用户代理池中随机抽取一个ua，实现反反爬
    user_agent = random.choice(headers_list)
    headers = {
        "User-Agent": user_agent,
        "Referer": "https://movie.douban.com/explore",
        "Cookie": cookie
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
    cookie = login()  # 登陆接口，如需要登陆，取消注释，去修改里面的用户名，密码即可
    if cookie:
        start_process(cookie)
    else:
        print('登录失败...')