import json, pymysql
from DBUtils.PooledDB import PooledDB

with open('config.json', 'r', encoding='utf-8') as f:
    mysql_config = json.loads(f.read())['mysql']
pool = PooledDB(pymysql, mincached=5, host=mysql_config['host'], user=mysql_config['username'],
                password=mysql_config['pwd'], database=mysql_config['db'], charset='utf8')
from logger import Logger

logger = Logger()


# 数据库插入，更新
def db_insert(sql):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        print(sql)
        cursor.execute(sql)
        conn.commit()
        logger.log("INFO", "数据插入, 更新", "数据库", "Admin")
    except Exception as ex:
        logger.log("ERROR", "数据插入, 更新错误, 原因:{}".format(ex), "数据库", "Admin")
        print('异常原因{}'.format(ex))
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# 数据库查询，返回查询结果
def db_query(sql):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        logger.log("INFO", "数据查询", "mysql", "Admin")
        return result
    except Exception as ex:
        logger.log("INFO", "数据查询错误, 原因: {}".format(ex), "mysql", "Admin")
        print('异常原因{}'.format(ex))
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    import datetime

    yesterday = datetime.date.today() + datetime.timedelta(-1)
    query_sql = "select order_sn, pdduid, accesstoken, notifyurl, orderno, amount, extends from order_pdd" \
                " where status='待发货' and is_query=1 and update_time like '{} %%'".format(yesterday)
    print(query_sql)
    result = db_query(query_sql)
    print(result)
