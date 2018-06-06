# -*- coding:utf-8 -*-
"""
author = zhangql
QQ = 1007228376
"""
import xlwt
import requests
from bs4 import BeautifulSoup
book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
sheet = book.add_sheet("Sheet")     # 添加Excel页签
sheet.write_merge(0, 0, 0, 7, 'python专属')
sheet.write(1, 0, 'all updates')
sheet.write(1, 1, 'all comments')
i = 2
j = 2


# 获取更新主函数
def get_update():
    global i
    headers = {
        "user-agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    url = 'https://www.kickstarter.com/projects/leagueofgeeks/armello-bringing-tabletop-adventures-to-life/updates'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    update_list = soup.find_all('a', class_='grid-post link hover-target')
    for update_ in update_list:
        update = update_.get_text().strip().replace('\n', '')
        sheet.write(i, 0, update)
        i += 1


# 获取评论主页面
def get_comment():
    headers = {
        "user-agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    url = 'https://www.kickstarter.com/projects/leagueofgeeks/armello-bringing-tabletop-adventures-to-life/comments'
    response = requests.get(url, headers=headers)
    parse_html(response.text)


# 解析每页的评论
def parse_html(html):
    global j
    soup = BeautifulSoup(html, 'html.parser')
    comment_list = soup.find_all('li')
    for comment_ in comment_list:
        comment = comment_.get_text().strip().replace('\n', '')
        sheet.write(j, 1, comment)
        j += 1
    try:
        url = 'https://www.kickstarter.com' + soup.find('a', class_='btn btn--light-blue btn--block mt3 older_comments')['href']
    except:
        return
    get_next_comment(url)


# 获取下一页的评论
def get_next_comment(url):
    headers = {
        "user-agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "referer": "https://www.kickstarter.com/projects/leagueofgeeks/armello-bringing-tabletop-adventures-to-life/comments"
    }
    response = requests.get(url, headers=headers)
    html = response.text
    parse_html(html)


if __name__ == '__main__':
    get_update()
    get_comment()
    path = r'文件.xls'
    book.save(path)