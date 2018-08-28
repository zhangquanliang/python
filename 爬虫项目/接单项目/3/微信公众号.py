# -*- coding:utf-8 -*-
__author__ = '张全亮'
import requests
import urllib3
import re
import datetime
import pymysql
pymysql.install_as_MySQLdb()
from multiprocessing.dummy import Pool
urllib3.disable_warnings()
headers = {
    "User-Agent": '[{"key":"User-Agent","value":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0","description":"","enabled":true}]',
    "Accept": "application/json",
    "Cookie": "rewardsn=; wxuin=1633977443; devicetype=android-25; version=26070237; lang=zh_CN; pass_ticket=KujmMeNVGQU/6j/ZtmJVtVHjNYy8N5eb3yAIlOSPch2iUMJgbMfJYZUeXySeiZFG; wap_sid2=COOIkosGElxBMHdqcXhhM2tXY0RfdzFBZllfT1V0Vm9Rbkc5LWd2dFNydkhySjJpR3JEVmcyV1ZoRnU1VmxsblFvZHJyUXEzWEUxVmRyVV9Xbk5wUm9SQzZoUVZFTXNEQUFBfjCNqojcBTgNQAE=; wxtokenkey=777"
}


def get_main_url_list():
    url = 'https://mp.weixin.qq.com/mp/homepage?__biz=MzA4NDI3NjcyNA==&hid=10&sn=2184f7554b5be7948a35c23705b4d72f&scene=18&devicetype=android-25&version=26070237&lang=zh_CN&nettype=WIFI&ascene=7&session_us=gh_6651e07e4b2d&pass_ticket=KujmMeNVGQU%2F6j%2FZtmJVtVHjNYy8N5eb3yAIlOSPch2iUMJgbMfJYZUeXySeiZFG&wx_header=1&begin=0&count=100&action=appmsg_list&f=json&r=0.83073623844131&appmsg_token='
    response = requests.post(url, headers=headers, verify=False)
    res_json = response.json()
    # pool = Pool(processes=30)
    for i in res_json['appmsg_list']:
        # pool.apply_async(get_comment, (i['appmsgid'], i['link'], i['title']))
        get_comment(i['appmsgid'], i['link'], i['title'])
    # pool.close()
    # pool.join()


def get_comment(appmsgid, article_url, article):
    response = requests.get(article_url, verify=False, headers=headers)
    comment_id = re.findall('var comment_id = "(.*?)" \|\|', response.text)[0]
    comment_url = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&__biz=MzA4NDI3NjcyNA==' \
                  '&appmsgid={}&idx=1&comment_id={}&offset=0&limit=100&uin=777&key=777&' \
                  'pass_ticket=KujmMeNVGQU%25252F6j%25252FZtmJVtVHjNYy8N5eb3yAIlOSPch2iUMJgbMfJYZUeXySeiZFG' \
                  '&wxtoken=777&devicetype=android-25&clientversion=26070237'.format(appmsgid, comment_id)
    comment_response = requests.get(comment_url, headers=headers, verify=False)
    print('文章[{}]有{}条评论'.format(article, len(comment_response.json()['elected_comment'])))
    for x in comment_response.json()['elected_comment']:
        nick_name = x['nick_name']
        content = x['content']
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into public_comment (article, article_url, nick_name, content, create_date) values ('{}', '{}','{}', '{}','{}')".format(article, article_url, nick_name, content, create_date)
        print(sql)
        db_insert(sql)


def db_insert(sql):
    conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='spider_j', charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        pass
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    get_main_url_list()