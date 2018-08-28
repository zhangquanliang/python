from flask import Flask, jsonify, request, redirect
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPTokenAuth
import hashlib
import pymysql
import json
import datetime
from mysql_db import db_insert

app = Flask(__name__)


# 爬虫部分
from pdd_spider import main
def spider(pdduid, accesstoken, goods_url):
    result = main(pdduid, accesstoken, goods_url)
    return result

@app.route('/')
def test():
    return 'server start success'

@app.route('/api/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'GET':
        return jsonify({'code': 0, 'msg': '请求方式必须为GET', 'order_sn': '', 'pay_url': ''})
    else:
        form_data = request.form.to_dict()
        check_data = ['accesstoken', 'amount', 'goods_url', 'orderno', 'pdduid', 'notifyurl', 'sign']
        for j in check_data:
            if j not in form_data:
                return jsonify({'code': 0, 'msg': 'POST参数错误', 'order_sn': '', 'pay_url': ''})
        if 'callbackurl' in form_data:
            callbackurl = form_data['callbackurl']
        else:
            callbackurl = ''
        if 'extends' in form_data:
            extends = form_data['extends']
        else:
            extends = ''

        accesstoken = form_data['accesstoken']  # 登陆的通讯令牌
        amount = form_data['amount']    # 金额,保持两位小数
        goods_url = form_data['goods_url']  # 自己家的商品地址
        orderno = form_data['orderno']    # 自己传入的订单号
        pdduid = form_data['pdduid']    # 登陆的手机号
        notifyurl = form_data['notifyurl']
        key = '2347647824628'   # 签名认证的key
        a = 'accesstoken={}&amount={}&goods_url={}&orderno={}&pdduid={}&key={}'.\
            format(accesstoken, amount, goods_url, orderno, pdduid, key)
        hl = hashlib.md5()
        hl.update(str(a).encode('utf-8'))
        encrypt = str(hl.hexdigest()).upper()
        print(encrypt)
        if form_data['sign'] == encrypt:
            result = spider(pdduid, accesstoken, goods_url)
            if result['code'] == 1:
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = "insert into order_pdd (accesstoken, amount, goods_url, orderno, pdduid, notifyurl, callbackurl," \
                      " extends, sign, order_type, pay_url, order_sn, status, is_query, create_time, update_time)" \
                      " values ('{}', '{}','{}', '{}','{}', '{}','{}', '{}', '{}','{}', '{}','{}', '{}', '{}','{}', '{}')". \
                    format(accesstoken, amount, goods_url, orderno, pdduid, notifyurl, callbackurl,
                           extends, encrypt, 'pdd', result['pay_url'],  result['order_sn'], '待支付', 1, create_time, create_time)
                db_insert(sql)
        else:
            result = {'code': 0, 'msg': '签名失败', 'order_sn': '', 'pay_url': ''}
        return jsonify(result)


# 设置路由，即路由地址为http://127.0.0.1:5000/api/pay
# api.add_resource(PddList, "/api/pay")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)