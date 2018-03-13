import os

from model import models
from model import model_manager

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


# 插入余额，传进数据字典或字典列表
def insert_balance(data):
    if not isinstance(data, list):
        data = [data]
    for i in data:
        obj = models.AccBalance.from_dict(**i)
        model_manager.AccBalanceManager.create_obj(obj)


# 插入流水，传进数据字典或字典列表
def insert_traded(data):
    if not isinstance(data, list):
        data = [data]
    for i in data:
        obj = models.AccTraded.from_dict(**i)
        model_manager.AccTradedManager.create_obj(obj)


# 插入账号信息(小账号，而不是登陆用的账号)，传进数据字典或字典列表
def insert_account(data):
    if not isinstance(data, list):
        data = [data]
    for d in data:
        obj = models.AccBaseInfo.from_dict(**d)
        #  先查询是否存在
        query = model_manager.session.query(models.AccBaseInfo).filter(models.AccBaseInfo.acc_number == d['acc_number'])
        if len(query.all()) > 0:
            keys = [i for i in d.keys()]
            for k in keys:
                if not hasattr(models.AccBaseInfo, k):
                    d.pop(k)
            if 'id' in d:
                d.pop('id')
            query.update(d)
            model_manager.session.commit()
        else:
            model_manager.AccBaseInfoManager.create_obj(obj)


# 插入登陆账号信息，传进数据字典或字典列表
def insert_login_user(data):
    if not isinstance(data, list):
        data = [data]
    for i in data:
        obj = models.LoginAcc.from_dict(**i)
        model_manager.LoginAccManager.create_obj(obj)


# 删除指定日期的余额,未指定acc_number则删指定日全部, del_date要用like格式 如 "2018-01-23%"
def del_balance_by_date(del_date=None, **kwargs):
    return model_manager.AccBalanceManager.fuzzy_query(del_date, **kwargs)


# 删除指定日期流水,未指定acc_number则删指定日全部，格式同上
# 不传date,则删除今天
def del_traded_by_date(del_date=None, **kwargs):
    return model_manager.AccTradedManager.fuzzy_query(del_date, **kwargs)


# 数据校验 根据login_info，去check,返回校验未通过的子账户的列表  参数为当前登录用户或者是批次号，账号
# 必须要传入账号
def check_data(acc_number):
    # 余额表最新余额和流水表最新余额校验
    acc_balance_manager = model_manager.AccBalanceManager  # 初始化一个余额表管理对象
    banlance_newest_balance = acc_balance_manager.get_newest_balance(acc_number)  # 获取余额表最新余额

    acc_traded_manager = model_manager.AccTradedManager  # 初始化一个流水表管理对象
    traded_newest_balance = acc_traded_manager.get_newest_balance(acc_number)

    # 流水表所有支出和收入与最初余额和最新余额差校验
    res1 = acc_traded_manager.get_traded_balance_infos(acc_number)
    res2 = acc_traded_manager.get_trarded_income_expend_infos(acc_number)
    if banlance_newest_balance == traded_newest_balance and res1 == res2:
        result = {
            "signal": 1,
            "msg1": "最新余额和流水最新余额匹配成功！",
            "msg2": "余额差和收入支出差匹配成功！"
        }
    else:
        result = {
            "signal": 0,
            "msg": "匹配失败！"
        }
    return result


# 校验流水表数据，返回出错的数据列表，列表内为字典，字典包含了错误数据的id和账号
def get_error_datas(**kwargs):
    acc_traded_manager = model_manager.AccTradedManager  # 实例化一个管理对象
    # 返回错误数据列表
    list = acc_traded_manager.get_error_data_list(**kwargs)
    return list


# 获取登陆账号信息,返回列表，每个元素为表t_login_info的字典
def get_login_info(bank_type, **kwargs):
    results = model_manager.session.query(models.LoginAcc).filter(models.LoginAcc.bank_type == bank_type).filter_by(**kwargs).all()
    return [result.to_dict() for result in results]


# 更新账号cookie之类,传入一个包含新cookie的login_info，查询更新
def update_authorization(authorization_dict):
    login_user = authorization_dict["login_user"]
    query = model_manager.session.query(models.LoginAcc).filter(models.LoginAcc.login_user == login_user)
    if len(query.all()) == 0:
        raise Exception("未匹配到登录名为[{}]的账户".format(login_user))
    elif len(query.all()) == 1:
        query.update(authorization_dict)
        model_manager.session.commit()
    else:
        raise Exception("数据库中匹配到登录名为[{}]账户数不唯一，请检查".format(login_user))


def query_accounts(bank_type):
    query = model_manager.session.query(models.AccBaseInfo).filter(models.AccBaseInfo.bank_type == bank_type)
    results = query.all()
    return [result.to_dict() for result in results]


def create_table():
    models.BaseModel.metadata.create_all(model_manager.engine)


if __name__ == '__main__':
    from model.models import AccBalance, AccTraded, AccBaseInfo
    from model.model_manager import session
    data = session.query(AccTraded).filter_by(bank_type='CEBS')
    list = []
    for i in data:
        print(i)
        list.append(i.acc_number)

    for acc in list:
        res = check_data(acc)
        print(res['signal'])
        print(res['msg1'])
        print(res['msg2'])

