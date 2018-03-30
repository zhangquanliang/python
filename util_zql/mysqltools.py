import pymysql

pymysql.install_as_MySQLdb()
import json


class MysqlTools(object):
    def __init__(self):
        self.host = ""
        self.port = ""
        self.db = ""
        self.user = ""
        self.password = ""
        self.charset = "utf8"

    # 读取数据库配置
    def __read_sql_config(self):
        with open("../config/dev.json") as f:
            data = json.loads(f.read())
            self.host = data['mysql']['host']
            self.db = data['mysql']['db']
            self.port = data['mysql']['port']
            self.user = data['mysql']['username']
            self.password = data['mysql']['pwd']

    # 获取连接和游标
    def __connect(self):
        self.__read_sql_config()
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db,
                                    user=self.user, password=self.password, charset=self.charset)

        self.cursor = self.conn.cursor()

    # 查询一条信息
    def fetchone(self, sql, params):
        try:
            self.__connect()
            self.cursor.execute(sql, params)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print("错误信息为====>", e)
        finally:
            self.__close()
        return None

    # 查询全部信息
    def fetchall(self, sql, params):
        try:
            self.__connect()
            self.cursor.execute(sql, params)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print("错误信息为=====>", e)
        finally:
            self.__close()

    # 增删改某条信息
    def update(self, sql, params):
        try:
            self.__connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            return count
        except Exception as e:
            print("错误信息是====>", e)
            self.conn.rollback()
        finally:
            self.__close()
        return 0

    # 关闭资源的方法
    def __close(self):
        if self.cursor != None:
            self.cursor.close()
        if self.conn != None:
            self.conn.close()
