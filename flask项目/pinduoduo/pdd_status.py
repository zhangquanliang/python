# -*- coding:utf-8 -*-
__author__ = '张全亮'
import requests
import urllib3
import hashlib
from multiprocessing.dummy import Pool
urllib3.disable_warnings()
import re, datetime, time, json
from logger import Logger
from mysql_db import db_query, db_insert
logger = Logger()


def check_pay(order_sn, pdduid, accesstoken):
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)
    headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': cookie
    }
    url = 'https://mobile.yangkeduo.com/personal_order_result.html?page=1&size=10&keyWord={}'.format(order_sn)
    res = requests.get(url, headers=headers, verify=False)
    # print(res.text)
    if 'window.isUseHttps= false' in res.text or 'window.isUseHttps' not in res.text:
        print('查询订单[{}]错误'.format(order_sn))
        logger.log('ERROR', '查询订单[{}]错误'.format(order_sn), 'status', pdduid)
        return '查询订单[{}]错误'.format(order_sn)
    else:
        n_order_sn = re.findall('"order_sn":"(.*?)",', res.text)[0]
        if order_sn == n_order_sn:
            pay_status = re.findall('"order_status_desc":"(.*?)",', res.text)[0]
            print('获取订单[{}]信息成功, 支付状态: {}'.format(n_order_sn, pay_status))
            logger.log('INFO', '获取订单[{}]信息成功, 支付状态: {}'.format(n_order_sn, pay_status), 'status', pdduid)
            return pay_status
        else:
            print('查询订单[{}]错误, 请确认!'.format(order_sn))
            logger.log('ERROR', '查询订单[{}]错误'.format(order_sn), 'status', pdduid)
            return '查询订单[{}]错误, 请确认!'.format(order_sn)


def main():
    query_sql = "select order_sn, pdduid, accesstoken, notifyurl, orderno, amount, extends from order_pdd" \
                " where status='待支付' and is_query=1 and u_id >= ((SELECT MAX(u_id) FROM order_pdd)-" \
                "(SELECT MIN(u_id) FROM order_pdd)) * RAND() + (SELECT MIN(u_id) FROM order_pdd) LIMIT 20"

    result = db_query(query_sql)
    print('查询数据库符合条件的结果, 共[{}]个'.format(len(result)))
    logger.log('INFO', '查询数据库符合条件的结果, 共[{}]个'.format(len(result)), 'status', '')
    if len(result) == 0:
        return
    pool = Pool(processes=20)
    for j in result:
        pool.apply_async(check, [j])
    pool.close()
    pool.join()


def check(result):
    for i in range(6):
        print('判断6分钟内, 订单编号为[{}]的订单, 支付状态是否已更改.'.format(result[0]))
        q_order_sn = result[0]
        pdduid = result[1]
        accesstoken = result[2]
        notifyurl = result[3]
        orderno = result[4]
        amount = result[5]
        extends = result[6]

        status = check_pay(q_order_sn, pdduid, accesstoken)
        if status != '待支付' and '错误' not in status:
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "update order_pdd set status='{}', is_query=0, update_time='{}'".format(status, update_time)
            db_insert(sql)
            key = 2347647824628
            a = 'amount={}&orderno={}&status={}&key={}'. \
                format(amount, orderno, status, key)
            hl = hashlib.md5()
            hl.update(str(a).encode('utf-8'))
            encrypt = str(hl.hexdigest()).upper()

            data = {
                "code": 1,
                "msg": "",
                "status": 1,
                "orderno": orderno,
                "amount": amount,
                "extends": extends,
                "sign": encrypt
            }
            for j in range(6):
                print('判断支付结果是否正常返回..')
                response = requests.post(notifyurl, data=data)
                if response.text == 'success':
                    logger.log('INFO', '订单[{}], 支付结果正常返回'.format(q_order_sn), 'status', pdduid)
                    break
                if j == 5:
                    logger.log('ERROR', '订单[{}], 支付结果未正常返回'.format(q_order_sn), 'status', pdduid)
                    break
                time.sleep(300)
            return
        if i == 5:
            print('订单编号为[{}]订单, 6分钟内订单支付状态未改变,仍为待支付,不在查询该订单.'.format(q_order_sn))
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "update order_pdd set status='{}', is_query=0, update_time='{}'".format(status, update_time)
            db_insert(sql)
            logger.log('DEBUG', '订单[{}], 设定时间内,支付状态未更改.'.format(q_order_sn), 'status', pdduid)
            return
        print('等待一分钟后重新判断待支付订单是否支付...共等待6分钟')
        time.sleep(60)


def test():
    order_sn = '180822-224630539190424'
    pdduid = '15179833772'
    accesstoken = 'N3NNUVW5BU6KXIK3PP6X44VO4X2MXE3ARUMZA6CBRAQQQ4SZXX6Q101a825'
    check_pay(order_sn, pdduid, accesstoken)


if __name__ == '__main__':
    print('检测订单脚本启动...')
    while True:
        main()
        time.sleep(10)
        # break