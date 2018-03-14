# -*- coding: utf-8 -*-
"""
sqlalchemy-连接数据库
"""
import pymysql
import datetime, time
pymysql.install_as_MySQLdb()
from model_zql.models import AccBalance, AccTraded
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def date_format_transform(date, date_format):
    date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, date_format)))
    return date


def get_engine():
    config = {
        "db_type": "mysql",
        "username": "root",
        "password": "zql9988",
        "host": "localhost",
        "port": "3306",
        "db": "zql_work"
    }

    db_type = config['db_type']     # 连接数据库类型Mysql，Oracle
    username = config['username']  # 用户名
    password = config['password']  # 密码
    host = config['host']           # IP
    port = config['port']            # 端口
    db = config['db']  # 需要连接的数据库
    s = "%s://%s:%s@%s:%s/%s?charset=utf8" % (db_type, username, password, host, port, db)
    return create_engine(s, echo=True)


# 由engine创建session
def create_session(engine):
    # 创建项目和数据库之间的会话对象
    db_session = sessionmaker(bind=engine)
    # 打开对话，返回会话对象
    return db_session()


# 数据模型基础操作类
class BaseManager(object):

    # 增加，插入
    @staticmethod
    def insert_obj(obj):
        session.add(obj)
        session.commit()
        return True

    # 删除,条件删除,query(对象),filter_by(条件)
    @staticmethod
    def delete_by_condition(obj, **kwargs):
        # 通过不确定参数去查询所有信息，然后删除
        result = session.query(obj).filter_by(**kwargs).all()
        for data in result:
            session.delete(data)
        session.commit()
        return True

    # 单查询,query(对象),filter_by(条件)
    @staticmethod
    def query_by_condition(obj, **kwargs):
        result = session.query(obj).filter_by(**kwargs)
        return result

    # 多查询,query(对象)
    @staticmethod
    def query_all(obj):
        result = session.query(obj).all()
        return result


# 登录账号模型管理类
class LoginAccManager(BaseManager):
    pass


# 账号模型管理类
class AccBaseInfoManager(BaseManager):
    pass


# 余额模型管理类
class AccBalanceManager(BaseManager):

    # 根据模糊查询余额
    @staticmethod
    def fuzzy_query(date=None, **kwargs):
        if not date:
            date = str(datetime.datetime.now())
            date = date[0:10]
        date = date_format_transform(date, '%Y-%m-%d')
        next_date = date + datetime.timedelta(days=1)
        data = session.query(AccBalance).filter(AccBalance.created_at > date).filter(
            AccBalance.created_at < next_date).filter_by(**kwargs)
        counts = len(data.all())
        for u in counts:
            session.delete(u)
        session.commit()
        session.close()
        return counts

    @staticmethod
    def get_newest_balance():
        data = session.query(AccBalance)
        id_list = []
        for u in data:
            id = u.id
            id_list.append(id)
        max_id = max(id_list)
        newest_data = session.query(AccBalance).filter_by(id=max_id)
        newest_balance = 0
        for u in newest_data:
            newest_balance = u.acc_balance
        return newest_balance


# 流水模型管理类
class AccTradedManager(BaseManager):
    # 按条件删除流水
    @staticmethod
    def fuzzy_query(date=None, **kwargs):
        if not date:
            date = str(datetime.datetime.now())
            date = date[0:10]
        date = date_format_transform(date, '%Y-%m-%d')
        next_date = date + datetime.timedelta(days=1)
        data = session.query(AccTraded).filter(AccTraded.acc_transaction_date > date).filter(
            AccTraded.acc_transaction_date < next_date).filter_by(**kwargs)
        counts = len(data.all())
        for u in data:
            session.delete(u)
        session.commit()
        session.close()
        return counts

    # 根据login_user/批次号/账号查询流水信息, 返回结果为流水对象列表
    @staticmethod
    def query_Acctraded(**kwargs):
        data = session.query(AccTraded).filter_by(**kwargs)
        # 空列表保存结果
        list = []
        for i in data:
            list.append(i)
        session.close()
        return list

    # 查询最新余额
    @staticmethod
    def get_newest_balance():
        data = session.query(AccTraded)
        id_list = []
        for u in data:
            id = u.id
            id_list.append(id)
        max_id = max(id_list)
        newest_data = session.query(AccTraded).filter_by(id=max_id)
        newest_balance = 0
        for u in newest_data:
            newest_balance = u.acc_balance
        return newest_balance

    # 按条件查询所有总收入和总支出的差
    @staticmethod
    def get_trarded_income_expend_infos(**kwargs):
        traded_datas = session.query(AccTraded).filter_by(**kwargs)
        income_sum = 0  # 收入和
        expend_sum = 0  # 支出和
        for data in traded_datas:
            income_sum = income_sum + data.acc_credit_money
            expend_sum = expend_sum + data.acc_drawee_money
        res = income_sum - expend_sum
        res = abs(res)
        return res

    # 获取条件查询余额表最初余额和最终余额差
    @staticmethod
    def get_traded_balance_infos(**kwargs):
        # 查询最初余额
        # 先按条件查出需要校验的数据集合
        datas = session.query(AccTraded).filter_by(**kwargs)
        # 获取集合的最小和最大id
        id_list = []
        for u in datas:
            id = u.id
            id_list.append(id)
        max_id = max(id_list)  # 最大id
        min_id = min(id_list)  # 最小id
        max_id_data = session.query(AccTraded).filter_by(id=max_id)
        newest_balance = 0
        for u in max_id_data:
            newest_balance = u.acc_balance
        min_id_data = session.query(AccTraded).filter_by(id=min_id)
        initial_balance = 0
        for u in min_id_data:
            balance = u.acc_balance  # 这不是最初的余额，最初余额等于该条记录加上/减去该条记录的收入/支出额
            if u.acc_drawee_money != 0:
                initial_balance = balance + u.acc_drawee_money
            if u.acc_credit_money != 0:
                initial_balance = balance - u.acc_credit_money
        res = newest_balance - initial_balance
        res = abs(res)
        return res

    # 返回出错数据账号列表
    @staticmethod
    def get_error_data_list(**kwargs):
        # 按条件查询要校验的数据集合
        datas = session.query(AccTraded).filter_by(**kwargs).order_by(AccTraded.id.asc())
        error_data_list = []
        for data in datas:
            balance1 = data.acc_balance  # 当前行数据的余额
            id = data.id  # 当前行id
            next_id = id + 1
            next_data = session.query(AccTraded).filter_by(id=next_id)  # 查询下一行的数据
            for u in next_data:
                # print("支出金额：", u.acc_drawee_money)
                # print("收入金额:", u.acc_credit_money)
                balance2 = u.acc_balance
                # print("下一行余额为：", balance2)
                next_balance = 0
                if u.acc_drawee_money == 0:
                    # print("账户收入金额为：", u.acc_credit_money)
                    next_balance = balance1 + u.acc_credit_money  # 正确的下一行余额
                    # print("计算后下一行余额应为：", next_balance)
                else:
                    # print("账户支出金额：", u.acc_drawee_money)
                    next_balance = balance1 - u.acc_drawee_money
                    # print("计算后下一行余额应为：", next_balance)
                if next_balance != balance2:
                    result = {
                        "acc_number": data.acc_number,
                        "id": data.id
                    }
                    error_data_list.append(result)
        return error_data_list


# 初始化数据库连接，创建连接引擎
engine = get_engine()
session = create_session(engine=engine)


if __name__ == '__main__':
    from model_zql.models import User
    # # 初始化数据库连接，创建连接引擎
    # engine = get_engine()
    # for i in range(2, 10):
    #     user = User(id=i, name='zhangql', age='22')
    #     session.add(user)
    result = session.query(User).all()
    print(result)
    for i in result:
        pass
        session.delete(i)
    session.commit()
    session.close()