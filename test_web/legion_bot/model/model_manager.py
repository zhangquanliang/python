import datetime
import json
import os

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import AccTraded, AccBalance
from util.tools import Tools

pymysql.install_as_MySQLdb()


# 读取数据库配置
def get_engine():
    current_path = os.path.dirname(os.path.realpath(__file__))
    current_path = "/".join(current_path.split("\\")) + "/"
    with open(current_path + "../config/dev.json") as f:
        res = json.loads(f.read())["oracle"]

    # 创建项目和数据库的连接引擎,通过引擎可以直接操作sql语句   create_engine的参数依次为数据库类型名、用户名、密码、IP、端口、数据库名
    s = "%s://%s:%s@%s:%s/%s?charset=utf8" % (
        res['db_type'], res['username'], res['pwd'], res['host'], res['port'], res['db'])
    return create_engine(s, echo=False)


# 由engine产生session
def create_session(engine):
    # engine = create_engine("mysql://root:password@127.0.0.1:3306/bank_db?charset=utf8", echo=False)

    # 创建项目和数据库之间的会话对象
    db_session = sessionmaker(bind=engine)

    # 打开对话，就可以通过session用sql语句操作数据库了
    return db_session()


engine = get_engine()
session = create_session(engine)


# 数据模型基础操作类
class BaseManager(object):
    # 增加
    @staticmethod
    def create_obj(params):
        session.add(params)
        session.commit()
        return True

    # 按条件删除
    def delete_by_condition(self, obj, **kwargs):
        data = session.query(obj).filter_by(**kwargs).all()
        for u in data:
            session.delete(u)
        session.commit()
        return True

    # 单查询
    def query_by_condition(self, obj, **kwargs):
        return session.query(obj).filter_by(**kwargs)

    # 多查询
    # def query_all(self, obj):

    @staticmethod
    def query_by_condition(obj, **kwargs):
        return session.query(obj).filter_by(**kwargs)

    # 多查询
    @staticmethod
    def query_all(obj):
        return session.query(obj).all()


# 登录账号模型管理类
class LoginAccManager(BaseManager):
    pass


# 账号模型管理类
class AccBaseInfoManager(BaseManager):
    pass


# 余额模型管理类
class AccBalanceManager(BaseManager):
    # 根据模糊查询删除余额

    @staticmethod
    def fuzzy_query(date=None, **kwargs):
        if not date:
            date = str(datetime.datetime.now())
            date = date[0:10]
        date = Tools.date_format_transform(date, '%Y-%m-%d')
        next_date = date + datetime.timedelta(days=1)
        data = session.query(AccBalance).filter(AccBalance.created_at > date).filter(
            AccBalance.created_at < next_date).filter_by(**kwargs)
        counts = len(data.all())
        for u in data:
            session.delete(u)
        session.commit()
        session.close()
        return counts

    # 获取最新余额，按照账号来查询数据
    @staticmethod
    def get_newest_balance(acc_num):
        data = session.query(AccBalance).filter_by(acc_number=acc_num)
        newest_balance = 0  # 最新余额
        for u in data:
            newest_balance = u.acc_balance  # 余额表只会有一条数据
        return newest_balance


# 流水模型管理类
class AccTradedManager(BaseManager):
    # 按条件删除流水
    @staticmethod
    def fuzzy_query(date=None, **kwargs):
        if not date:
            date = str(datetime.datetime.now())
            date = date[0:10]
        date = Tools.date_format_transform(date, '%Y-%m-%d')
        next_date = date + datetime.timedelta(days=1)
        data = session.query(AccTraded).filter(AccTraded.created_at > date).filter(
            AccTraded.created_at < next_date).filter_by(**kwargs)
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
    def get_newest_balance(acc_num):
        data = session.query(AccTraded).filter_by(acc_number=acc_num)
        id_list = []  # 流水表会有很多条记录，选取id最大的就是最新的
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
    def get_trarded_income_expend_infos(acc_num):
        traded_datas = session.query(AccTraded).filter_by(acc_number=acc_num)
        income_sum = 0  # 收入和
        expend_sum = 0  # 支出和
        for data in traded_datas:
            income_sum = income_sum + data.acc_credit_money
            expend_sum = expend_sum + data.acc_drawee_money
        res = income_sum - expend_sum
        res = abs(res)  # 收入支出差
        return res

    # 获取条件查询余额表最初余额和最终余额差
    @staticmethod
    def get_traded_balance_infos(acc_num):
        # 查询最初余额
        # 先按条件查出需要校验的数据集合
        datas = session.query(AccTraded).filter_by(acc_number=acc_num)
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
            newest_balance = u.acc_balance  # 该账号最新余额
        min_id_data = session.query(AccTraded).filter_by(id=min_id)
        initial_balance = 0
        for u in min_id_data:
            balance = u.acc_balance  # 这不是最初的余额，最初余额等于该条记录加上/减去该条记录的收入/支出额
            if u.acc_drawee_money != 0:
                initial_balance = balance + u.acc_drawee_money  # 该账号最初余额
            if u.acc_credit_money != 0:
                initial_balance = balance - u.acc_credit_money  # 该账号最初余额
        res = newest_balance - initial_balance  # 最新余额和最初余额差
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
                    result = {"acc_number": data.acc_number, "id": data.id}
                    error_data_list.append(result)
        return error_data_list


if __name__ == '__main__':
    from model.models import AccBalance, AccTraded, AccBaseInfo

    data = session.query(AccBalance).filter_by(bank_type='CEBS')
    list = []
    for i in data:
        print(i)
        list.append(i)
        # session.delete(i)
        # session.commit()

    print(len(list))
