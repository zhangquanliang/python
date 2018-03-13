import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def datetime_to_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def str_to_datetime(st):
    return datetime.strptime(st, "%Y-%m-%d %H:%M:%S")


# 需要特殊处理的时间字段，键为数据库名dbf，值为json返回值jsonf

rename_fields = {
    'created_at': 'createAt',
    'updated_at': 'updateAt',
    'deleted_at': 'deleteAt',
}

# 创建的对象的基类
BaseModel = declarative_base()


class ModelProcessor:
    def to_dict(self):
        dict_ = {}
        for filed in self.__get_fields():
            dict_[filed] = getattr(self, filed)
        for old, new in rename_fields.items():
            if isinstance(getattr(self, old), datetime):
                dict_[new] = datetime_to_str(dict_[old])
            else:
                dict_[new] = None
            dict_.pop(old)
        return dict_

    @classmethod
    def from_dict(cls, **dict_):
        fields = cls.__get_fields()
        for dbf, jf in rename_fields.items():
            if jf in dict_:
                dict_.pop(jf)
                dict_[dbf] = None
        for k in list(dict_):
            assert type(dict_[k]) in [str, float, type(None)], '{}字段数据类型不能为{}，只能为str或None'.format(k, type(dict_[k]))
            if isinstance(fields[k], DateTime) and dict_[k]:
                dict_[k] = str_to_datetime(dict_[k])
        return cls(**dict_)

    @classmethod
    def __get_fields(cls):
        return {f: getattr(cls, f).expression.type for f in cls._sa_class_manager._all_key_set}


# # 登录账号模型
class LoginAcc(BaseModel, ModelProcessor):
    __tablename__ = "t_login_info"

    id = Column(Integer, primary_key=True)  # id主键
    bank_type = Column(String(255), nullable=False)  # 银行类型
    login_user = Column(String(255), nullable=False)  # 账号
    login_password = Column(String(255), nullable=False)  # 密码
    login_extend1 = Column(String(255), nullable=True)  # 登录扩展字段1
    login_extend2 = Column(String(255), nullable=True)  # 登录扩展字段2
    login_extend3 = Column(String(255), nullable=True)  # 登录扩展字段3
    login_extend4 = Column(String(255), nullable=True)  # 登录扩展字段4
    authorization_cookie = Column(String(255), nullable=True)  # 认证cookie
    authorization_extend1 = Column(String(255), nullable=True)  # 认证扩展字段1
    authorization_extend2 = Column(String(255), nullable=True)  # 认证扩展字段2
    authorization_extend3 = Column(String(255), nullable=True)  # 认证扩展字段3
    authorization_extend4 = Column(String(255), nullable=True)  # 认证扩展字段4
    update_date = Column(DateTime, nullable=True)  # 创建时间
    remark = Column(String(255), nullable=True)  # 备注拓展说明

    def to_dict(self):
        dict_ = {}
        for filed in self.__get_fields():
            dict_[filed] = getattr(self, filed)
        return dict_

    @classmethod
    def __get_fields(cls):
        return {f: getattr(cls, f).expression.type for f in cls._sa_class_manager._all_key_set}



# 账户模型
class AccBaseInfo(BaseModel, ModelProcessor):
    __tablename__ = "t_acc_baseinfo"

    id = Column(Integer, primary_key=True)  # id主键
    bank_type = Column(String(255), nullable=False)  # 银行类型
    acc_number = Column(String(255), nullable=True)  # 账号
    acc_name = Column(String(255), nullable=True)  # 账号名称
    acc_status = Column(String(255), nullable=True)  # 账号状态
    acc_type = Column(String(255), nullable=True)  # 账号类型
    acc_info = Column(String(255), nullable=True)  # 平安查询余额所需的参数
    acc_open_bank_name = Column(String(255), nullable=True)  # 开户行
    acc_author = Column(String(255), nullable=True)  # 当前登录账号
    acc_id = Column(String(255), nullable=True)  # 托管产品代码(兴业)
    login_user = Column(String(255), nullable=True)  # 来自登陆账号
    combination_name = Column(String(255), nullable=True)  # 组合名称
    project_id = Column(String(255), nullable=True)  # 项目id
    created_at = Column(DateTime, nullable=True)  # 数据创建时间
    updated_at = Column(DateTime, nullable=True)  # 更新时间
    deleted_at = Column(DateTime, nullable=True)  # 删除时间
    build_at = Column(DateTime, nullable=True)  # 开户时间
    end_at = Column(DateTime, nullable=True)  # 项目结束时间

    def __init__(self, **kwargs):
        kwargs['created_at'] = datetime.now()
        super().__init__(**kwargs)


# 余额模型
class AccBalance(BaseModel, ModelProcessor):
    __tablename__ = "t_acc_balance"

    id = Column(Integer, primary_key=True)
    bank_type = Column(String(255), nullable=False)  # 银行类型
    acc_number = Column(String(255), nullable=True)  # 账号
    acc_name = Column(String(255), nullable=True)  # 账号名称
    acc_type = Column(String(255), nullable=True)  # 账号类型
    acc_currency = Column(String(255), nullable=True)  # 币种
    acc_balance = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=False)  # 账号余额
    acc_freeze_balance = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2),
                                nullable=True)  # acc_freeze_balance
    acc_available_balance = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 可用余额
    acc_open_bank_name = Column(String(255), nullable=True)  # 开户网点(民生)
    acc_begin_date = Column(DateTime, nullable=True)  # 开户日
    acc_status = Column(String(255), nullable=True)  # 状态(建行,民生,招商U)
    acc_control_status = Column(String(255), nullable=True)  # 账户控制状态
    acc_book_balance = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 账面余额
    acc_okay_bye = Column(String(255), nullable=True)  # 行别
    acc_daily_balance = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 末笔交易上日余额
    deposit_type = Column(String(255), nullable=True)  # 存款类型
    acc_id = Column(String(255), nullable=True)  # 托管产品代码
    acc_interestrate = Column(String(255), nullable=True)  # 利率(%)
    currency_type_code = Column(String(255), nullable=True)  # 货币类型_代码
    account_state_code = Column(String(255), nullable=True)  # 账户状态_代码
    combination_name = Column(String(255), nullable=True)  # 工商组合名称
    interestrate_model = Column(String(255), nullable=True)  # 利率方式(邮储)
    interestrate_project = Column(String(255), nullable=True)  # 利率项目(邮储)
    agreement_base = Column(String(255), nullable=True)  # 协定基数(邮储)
    acc_balance_date = Column(DateTime, nullable=True)  # 余额日期
    acc_income = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 收入
    acc_expenditure = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 支出
    login_user = Column(String(255), nullable=True)  # 来自登陆账号
    batch_id = Column(String(255), nullable=True)  # 批次号
    created_at = Column(DateTime, nullable=True, default=datetime.now())  # 创建时间
    updated_at = Column(DateTime, nullable=True)  # 更新时间
    deleted_at = Column(DateTime, nullable=True)  # 删除时间

    def __init__(self, **kwargs):
        kwargs['created_at'] = datetime.now()
        super().__init__(**kwargs)


class AccTraded(BaseModel, ModelProcessor):
    __tablename__ = "t_acc_traded_list"

    id = Column(Integer, primary_key=True)  # 主键
    bank_type = Column(String(255), nullable=False)  # 银行类型(如ICBank 指工商银行)
    acc_number = Column(String(255), nullable=True)  # 账号
    acc_transaction_time = Column(DateTime, nullable=True)  # 交易时间
    acc_transaction_date = Column(DateTime, nullable=True)  # 交易日期
    acc_transaction_type = Column(String(255), nullable=True)  # 交易类型
    acc_business_type = Column(String(255), nullable=True)  # 业务类型
    acc_currency = Column(String(255), nullable=True)  # 币种
    acc_voucher_number = Column(String(255), nullable=True)  # 凭证号
    acc_voucher_type = Column(String(255), nullable=True)  # 凭证类型
    acc_revenue_expenditure = Column(String(255), nullable=True)  # 收支方向
    acc_drawee_money = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 借方发生额
    acc_credit_money = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 贷方发生额
    acc_balance = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 账户余额
    acc_opposite_number = Column(String(255), nullable=True)  # 对方账号
    acc_opposite_name = Column(String(255), nullable=True)  # 对方户名
    acc_opposite_open_name = Column(String(255), nullable=True)  # 对方开户机构(华润，新业)
    acc_abstract = Column(String(255), nullable=True)  # 摘要
    acc_remarks = Column(String(255), nullable=True)  # 备注
    acc_pay_use = Column(String(255), nullable=True)  # 用途
    acc_opposite_no = Column(String(255), nullable=True)  # 对方行号
    acc_start_interest = Column(DateTime, nullable=True)  # 起息日期
    acc_exchange_rate = Column(String(255), nullable=True)  # 汇率(%)(中国)
    acc_transaction_no = Column(String(255), nullable=True)  # 交易流水号
    acc_customer_no = Column(String(255), nullable=True)  # 客户申请号(中国)
    acc_customer_number = Column(String(255), nullable=True)  # 客户业务编号(中国)
    acc_record_identifier = Column(String(255), nullable=True)  # 记录标识号(中国)
    acc_traded_code = Column(String(255), nullable=True)  # 交易分析码(招商)
    acc_author = Column(String(255), nullable=True)  # 账户持有账号(招商)
    acc_tran_desc = Column(String(255), nullable=True)  # 处理方式(华润)
    acc_charge_fee = Column(DECIMAL(precision=16, scale=2, decimal_return_scale=2), nullable=True)  # 费用(华润)
    account_type_show = Column(String(255), nullable=True)  # 账户展示类型(华润)
    acc_end_interest = Column(String(255), nullable=True)  # 结息(华润)
    acc_id = Column(String(255), nullable=True)  # 兴业托管产品代码
    batch_id = Column(String(255), nullable=True)  # 批次号
    created_at = Column(DateTime, nullable=True, default=datetime.now())  # 创建时间
    updated_at = Column(DateTime, nullable=True)  # 更新时间
    deleted_at = Column(DateTime, nullable=True)  # 删除时间
    login_user = Column(String(255), nullable=False)  # 子账号归属用户

    def __init__(self, **kwargs):
        kwargs['created_at'] = datetime.now()
        super().__init__(**kwargs)


if __name__ == '__main__':
    pass
    # create_table()

    base = AccBaseInfo(
        bank_type='test_type',
        acc_number='1234654798',
        acc_name='属羊2号',
    )
    # print(base.created_at)
    # print(base.to_dict()['createAt'])
    # fields = base.get_fields()
    # print(fields)
    pass

