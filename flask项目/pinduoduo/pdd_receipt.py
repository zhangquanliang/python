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


def evaluation(pdduid, accesstoken, goods_id, order_sn):
    url = 'https://mobile.yangkeduo.com/proxy/api/v2/order/goods/review?pdduid={}'.format(pdduid)
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)
    headers = {
        'accesstoken': accesstoken,
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': cookie
    }
    data = {
        "goods_id": goods_id,
        "order_sn": order_sn,
        "desc_score": 5,
        "logistics_score": 5,
        "service_score": 5,
        "comment": "商品特别好，已经买过很多次了.",
        "pictures": [],
        "labels": []
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if 'review_id' in response.json() and 'share_code' in response.json():
        return True
    else:
        return False


# 确认收货
def confirm_receipt(accesstoken, pdduid, order_sn):
    url = 'https://mobile.yangkeduo.com/proxy/api/order/{}/received?pdduid={}&is_back=1'.format(order_sn, pdduid)
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)
    headers = {
        'accesstoken': accesstoken,
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': cookie
    }
    response = requests.post(url, headers=headers, verify=False)
    if 'nickname' in response.json() and 'share_code' in response.json():
        return True
    else:
        return False


def check_pay(order_sn, pdduid, accesstoken):
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)
    headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': cookie
    }
    url = 'https://mobile.yangkeduo.com/personal_order_result.html?page=1&size=10&keyWord={}'.format(order_sn)
    res = requests.get(url, headers=headers, verify=False)

    if 'window.isUseHttps= false' in res.text or 'window.isUseHttps' not in res.text:
        logger.log('ERROR', '查询订单[{}]错误'.format(order_sn), 'receipt', pdduid)
        return '查询订单[{}]错误'.format(order_sn)
    else:
        n_order_sn = re.findall('"order_sn":"(.*?)",', res.text)[0]
        if order_sn == n_order_sn:
            pay_status = re.findall('"order_status_desc":"(.*?)",', res.text)[0]
            logger.log('INFO', '获取订单[{}]信息成功, 支付状态: {}'.format(n_order_sn, pay_status), 'receipt', pdduid)
            return pay_status
        else:
            logger.log('ERROR', '查询订单[{}]错误'.format(order_sn), 'receipt', pdduid)
            return '查询订单[{}]错误, 请确认!'.format(order_sn)


def check(result):
    logger.log('INFO', '开始校验订单:{}支付状态'.format(result[0]), 'receipt', result[1])
    q_order_sn = result[0]
    pdduid = result[1]
    accesstoken = result[2]
    goods_id = result[3]

    status = check_pay(q_order_sn, pdduid, accesstoken)
    if '待收货' in status and '错误' not in status:
        if confirm_receipt(accesstoken, pdduid, q_order_sn):
            logger.log('INFO', '订单[{}]已确认收货'.format(q_order_sn), 'receipt', pdduid)
            if evaluation(pdduid, accesstoken, goods_id, q_order_sn):
                logger.log('INFO', '订单[{}]已5星好评'.format(q_order_sn), 'receipt', pdduid)
            else:
                logger.log('DEBUG', '订单[{}]5星好评错误'.format(q_order_sn), 'receipt', pdduid)
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "update order_pdd set status='{}', is_query=0, update_time='{}' where order_sn='{}'". \
                format('已评价', update_time, q_order_sn)
            db_insert(sql)
        else:
            logger.log('ERROR', '订单[{}]收货错误'.format(q_order_sn), 'receipt', pdduid)


def main():
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    query_sql = "select order_sn, pdduid, accesstoken, goods_id from order_pdd" \
                " where status='待发货' and is_query=1 and update_time like '{} %%'".format(yesterday)
    # query_sql = "select order_sn, pdduid, accesstoken, goods_id from order_pdd" \
    #             " where status='待发货' and is_query=1 "
    result = db_query(query_sql)
    logger.log('INFO', '查询数据库符合条件的结果, 共[{}]个'.format(len(result)), 'receipt', 'Admin')
    if len(result) == 0:
        return
    pool = Pool(processes=20)
    for j in result:
        pool.apply_async(check, [j])
    pool.close()
    pool.join()


if __name__ == '__main__':
    logger.log('INFO', '确认收货脚本启动...', 'receipt', 'Admin')
    while True:
        try:
            main()
        except:
            logger.log('ERROR', '程序异常，重启.', 'receipt', 'Admin')
            continue
        time.sleep(30)
        # break
