# -*- coding: utf-8 -*-
"""
Title = 全书网小说
Date = 2018-03-02
"""
import re
import requests
import pymysql
from multiprocessing import Pool
# conn = pymysql.Connect(
#     host='localhost',   # ip
#     port=3306,    # 端口
#     user='root',  # 账号
#     password='zql9988',   # 密码
#     db='zql_work',  # 数据库名
#     charset='utf8',  # 编码
# )
# cursor = conn.cursor()  # 游标
#

# 定义小说分类列表的函数
def get_novel_sort_list():
    response = requests.get(url='http://www.quanshuwang.com/list/1_1.html')
    response.encoding = 'gbk'
    reslut = response.text
    reg = r'<a target="_blank" title=".*" href="(.*?)" class="clearfix stitle">(.*?)</a>'
    nover_url_list = re.findall(reg, reslut)
    return nover_url_list

# 定义小说章节地址
def get_novel_content(url):
    # requests = requestsuests.session()
    response = requests.get(url=url)
    response.encoding = 'gbk'
    reslut = response.text
    reg = r'<a href="(.*?)" class="reader" title=".*?">开始阅读</a>'
    novel_url = re.findall(reg, reslut)[0]
    return novel_url

# 定义小说阅读地址
def get_chapter_url_list(url):
    response = requests.get(url=url)
    response.encoding = 'gbk'
    result = response.text
    reg = r'<li><a href="(.*?)" title="(.*?)">.*?</a></li>'   # 加r原生字符
    chapter_url_list = re.findall(reg, result)
    return chapter_url_list

# 定义小说内容
def get_chapter_content(url):
    # requests = requestsuests.session()
    response = requests.get(url=url)
    response.encoding = 'gbk'
    result = response.text
    reg = r'style5\(\);</script>(.*?)<script type="text/javascript">style6\(\)'   # 此处加\为正则匹配使用
    chapter_content = re.findall(reg, result, re.S)[0]  # re.S可进行换行匹配
    return chapter_content


for novel_url, novel_name in get_novel_sort_list():  # novel_url小说地址  novel_name小说名字
    novel_count_url = get_novel_content(novel_url)
    for chapter_url, chapter_name in get_chapter_url_list(novel_count_url):   # chapter_url小说章节地址 chapter_name小说节名字
        # cursor.execute("insert into novel(novel_name, novel_url, chapter_name, chapter_url) "
        #                "values('%s','%s','%s','%s')" % (novel_name, novel_url, chapter_name, chapter_url))
        # conn.commit()  # 事务提交  conn.rollback() 事务回滚
        try:
            print(novel_name, chapter_name)
            chapter_content = (get_chapter_content(chapter_url))   # content 小说内容
            # cursor.execute("insert into chapter(chapter_name, chapter_content) values('%s','%s')"  % (chapter_name, chapter_content))
            # conn.commit()
        except:
            print('小说章节%s暂时无法获取, 地址%s'% (chapter_name, chapter_url))
# cursor.close()
# conn.close()
