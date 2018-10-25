import json, pymysql
from DBUtils.PooledDB import PooledDB

with open('config.json', 'r', encoding='utf-8') as f:
    mysql_config = json.loads(f.read())['mysql']
pool = PooledDB(pymysql, mincached=5, host=mysql_config['host'], user=mysql_config['username'],
                password=mysql_config['pwd'], database=mysql_config['db'], charset='utf8')


# 数据库查询，返回查询结果
def db_query(sql):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as ex:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()