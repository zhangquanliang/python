# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import time, random,string,redis,os,sys, datetime
cur_path = os.path.abspath(__file__)
base_path = os.path.dirname(os.path.dirname(cur_path))
sys.path.insert(0,base_path)
from configsetting import REDIS_IP,REDIS_PORT, LAST_NAME, FIRST_NAME, STATE_CODE


def get_bornDate():
    """返回一个随机生成的'19880914'这样格式的日期"""
    date_time = datetime.datetime.now().strftime("%Y%m%d")
    return date_time


def get_IdCard(u_card):
    """返回一个包含某个地区的18位身份证号和地区名称的元组(idcard,state)"""
    src_num = string.digits
    src_c = string.digits + 'X'
    dic = STATE_CODE[random.randint(0, len(STATE_CODE))]
    idcard = dic['code'] + get_bornDate() + ''.join(random.sample(src_num, 3)) + ''.join(random.sample(src_c, 1))
    if idcard in u_card:  # 如果生成的身份证redis已存在，则重新生成
        get_IdCard(u_card)
    else:
        return idcard


def get_name():
    """ 返回一个随机生成的姓名 """
    l_name = random.choice(LAST_NAME)
    # firstname 随机取1-2个汉子
    count = random.randint(1, 2)
    if count == 1:
        f_name = random.choice(FIRST_NAME)
    else:
        f_name = random.choice(FIRST_NAME) + random.choice(FIRST_NAME)
    name = l_name + f_name
    return name


count = input("请输入你要生成名字和身份证的数量：\n").strip()
for i in range(int(count)):
    r = redis.Redis(host=REDIS_IP, port=REDIS_PORT,  decode_responses=True)  # 获取数据
    name = get_name()
    user = r.hgetall('user')
    u_card = []
    for k in user:
        u_card.append(user[k])
    new_id = get_IdCard(u_card)
    r.hset('user', name, new_id)