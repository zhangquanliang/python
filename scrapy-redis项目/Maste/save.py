# -*- coding:utf-8 -*-
import pymysql
import redis
import datetime

r = redis.Redis(host='120.55.48.59', port=6379)


# 数据库连接入库
def db_insert(sql):
    conn = pymysql.connect(host='localhost', user='root', password='MyNewPass4!', database='youzan', charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        print('保存1000条记录成功...')
    except:
        pass
    finally:
        cursor.close()
        conn.close()


def main():
    result_list = r.lrange('book', 0, 1000)
    r.ltrim('book', 1001, -1)
    if not result_list:
        return
    sql = "INSERT INTo t_novel_test (novel_name, chapter_name, context, novel_type, chapter_url, create_date) " \
          "VALUES"
    for result in result_list:
        q_result = eval(result)
        novel_name = q_result['novel_name']
        chapter_name = q_result['chapter_name']
        context = q_result['context']
        novel_type = q_result['novel_type']
        chapter_url = q_result['chapter_url']
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql += "(" + "'" + str(novel_name) + "'" + "," + \
                            "'" + str(chapter_name) + "'" + "," +\
                            "'" + str(context) + "'" + "," + \
                            "'" + str(novel_type) + "'" + "," + \
                            "'" + str(chapter_url) + "'" + "," + \
                            "'" + str(create_date) + "'" + ")" + ","
    db_insert(sql[:-1])


if __name__ == '__main__':
    while True:
        main()
