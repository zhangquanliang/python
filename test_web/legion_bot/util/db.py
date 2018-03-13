# -*- coding: utf-8 -*-
import sys
import os
import datetime
import importlib
importlib.reload(sys)
import sys
import cx_Oracle

from DBUtils.PooledDB import PooledDB
# from tools import get_setting
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# sys.setdefaultencoding('utf-8')


class DataBaseOperator(object):
    # 连接池对象
    __pool = None

    def __init__(self):

        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = DataBaseOperator.__get_conn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __get_conn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if DataBaseOperator.__pool is None:
            __pool = PooledDB(cx_Oracle, 5, user="crbot", password="crbot123", dsn="10.132.122.25:1521/orcl")
        return __pool.connection()

    def insert_table(self, sql):
        self._cursor.execute(sql)
        self._conn.commit()
        return

    def query_table(self, sql):
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def save_authorization(self, auth_key, auth_value, user_id=None):
        update_time = datetime.datetime.now()
        sql = "select auth_value from t_cr_authorization where auth_key = '%s'" % auth_key
        if user_id:
            sql = "%s and user_id = '%s'" % (sql, user_id)
        result = self.query_table(sql)
        if len(result) == 0:
            sql = "insert into t_cr_authorization (auth_key, auth_value, user_id, update_time)" \
                  " values ('%s','%s','%s', '%s')" \
                  % (auth_key, auth_value, user_id, update_time)
        else:
            sql = "update t_cr_authorization set auth_value = '%s',update_time = '%s' where auth_key = '%s'" \
                  % (auth_value, update_time, auth_key)
            if user_id:
                sql = "%s and user_id = '%s'" % (sql, user_id)

        self.insert_table(sql)
        return

    def get_authorization(self, auth_key, user_id=None):
        sql = "select auth_value from t_cr_authorization where auth_key = '%s' " % auth_key
        if user_id:
            sql = "%s and user_id='%s'" % (sql, user_id)
        sql = sql + " order by update_time desc"
        result = self.query_table(sql)
        if len(result) > 0:
            return result[0][0]
        else:
            return None


if __name__ == "__main__":
    db_operator = DataBaseOperator()
    print(db_operator.query_table("select 1 from dual"))

