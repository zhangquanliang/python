# -*- coding:utf-8 -*-
__author__ = '张全亮'

import requests
import time
import random
"""
pdduid = 用户ID
goods_id = 商品ID

"""

headers = {
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Host": "apiv3.yangkeduo.com",
        "Content-Type": "application/json;charset=UTF-8",
        "ETag": "hVblFHs0",
        "Cookie": "api_uid=rBQ5E1t3gjt2DBr0M+HLAg==",
        "AccessToken": "VCXGJT7JXGS2DQO4UIWDW2QAVM3L44ZG6DGSKXX6UV5Q24ISDY4A103f980",
        "User-Agent": "android Mozilla/5.0 (Linux; Android 7.1.1; vivo X20Plus UD Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36  phh_android_version/4.18.1 phh_android_build/f46e67a29b phh_android_channel/yyb",
    }

# TODO
def zhifu(goods_id, group_id, sku_id):
    ts = int(time.time() * 1000)
    headers[
        'Referer'] = 'file:///order_checkout.html?goods_id={}&ts={}&goods_number=1&group_id={}&sku_id={}'.format(
        goods_id, ts, group_id, sku_id)
    # print(headers)
    url = 'http://apiv3.yangkeduo.com/order/prepay?pdduid=7387172857'
    j_data = {
        'order_sn': '180818-334506885854089',
        'app_id': '4',
        'pap_pay': '1',
        'version': '2',
        'attribute_fields': {"paid_times": 0}
    }
    # n_data = str(j_data).replace('"', "'").replace("'", '"')
    res = requests.post(url, verify=False, headers=headers, json=j_data)
    print(res.text)
    print(res.url)


def shangpin():
    url = 'http://apiv4.yangkeduo.com/api/oakstc/v15/goods/1090541921?goods_id=1090541921&from=0&pdduid=7387172857'
    # url = 'http://apiv4.yangkeduo.com/api/oakstc/v15/goods/67766752?goods_id=67766752&from=0&pdduid=7387172857'
    headers['Referer'] = 'Android'
    response = requests.get(url, headers=headers)
    json_str = response.json()
    print(json_str)
    goods_id = json_str['goods_id']
    print(goods_id)
    group_id = json_str['group'][random.randint(0, len(json_str['group']))]['group_id']
    sku_id = json_str['sku'][random.randint(0, len(json_str['sku']))]['sku_id']
    print(goods_id, group_id, sku_id)
    return goods_id, group_id, sku_id

# 接收goods_id,group_id,sku_id,
def xiadan(goods_id,group_id,sku_id):
    ts = int(time.time() * 1000)
    print(ts)
    headers[
    'Referer'] = 'file:///order_checkout.html?goods_id=1090541921&ts={}&goods_number=1&group_id=1454233618&sku_id=35926585586'.format(
    ts)
    # headers[
    # 'Referer'] = 'file:///order_checkout.html?goods_id={}&ts={}&goods_number=1&group_id={}&sku_id={}'.format(
    # goods_id, ts, group_id, sku_id)
    url = 'http://apiv3.yangkeduo.com/api/morgan/confirm/render?pdduid=7387172857'
    j_data = {
        "front_env":5,"front_version":1,"goods_id": goods_id,"group_id": group_id,"sku_id": sku_id,"goods_number":1,"address_id":"","is_app":1,"page_from":0,"type":0,"award_type":0,"biz_type":0
        }
    res = requests.post(url, headers=headers, json=j_data)
    print(res.json())

goods_id, group_id, sku_id  = shangpin()
xiadan(goods_id, group_id, sku_id)
zhifu(goods_id, group_id, sku_id)