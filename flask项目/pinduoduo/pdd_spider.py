# -*- coding:utf-8 -*-
__author__ = '张全亮'

# TODO 需要提供goods_url(商品地址), pdduid(拼多多用户ID,可为手机号), accesstoken(websocket加载的token)

"""
goods_url = 商品地址
goods_id = 商品ID
group_id = 分组排序ID
sku_id = 商品的属性ID,如衣服的尺码，颜色
cookie = 需要登陆状态下的Cookie
accesstoken = 支付认证的token
pdduid  = 拼多多用户ID
order_sn = 订单编号
"""

import re
import random
import urllib3
import requests
import urllib.parse
import time

urllib3.disable_warnings()
req = requests.session()
import pymysql
import json
import datetime
from logger import Logger

pymysql.install_as_MySQLdb()

logger = Logger()

headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
}

"""
获取商品需要的参数
input = 商品地址(goods_url), 登陆状态下的Cookie(cookie)
output = 分组排序ID(group_id), 商品ID(goods_id), 商品的属性ID(sku_id)如衣服的尺码，颜色
"""


def get_goods_id(url, cookie=None):
    res = requests.get(url, headers=headers, verify=False)
    html = res.text
    if cookie is not None:
        headers['Cookie'] = cookie
    sku_id = random.choice(re.findall('"skuID":(.*?),', html))
    group_id = random.choice(re.findall('"groupID":(.*?),', html))
    goods_id = random.choice(re.findall('"goodsID":"(.*?)",', html))
    return sku_id, group_id, goods_id


"""
获取需要的地址ID
input = 分组排序ID(group_id), 商品ID(goods_id), 商品的属性ID(sku_id)如衣服的尺码，颜色 购买数量(goods_number)
output = 地址ID(addressId)
"""


def get_address_id(sku_id, group_id, goods_id, goods_number=1):
    url = 'https://mobile.yangkeduo.com/order_checkout.html?sku_id={}&group_id={}&goods_id={}&goods_number={}'.format(
        sku_id, group_id, goods_id, goods_number)
    res = requests.get(url, headers=headers, verify=False)
    if 'window.isUseHttps= false' in res.text or 'window.isUseHttps' not in res.text:
        return '获取地区ID错误, 请更新AccessToken后重试..'
    html = res.text
    addressId = re.findall('"addressId":(.*?),', html)[0]
    return addressId


"""
input = 分组排序ID(group_id), 商品ID(goods_id), 商品属性ID(sku_id), 用户ID(pdduid), 
支付宝登陆成功认证的token(accesstoken), 地址ID(address_id)
output = 付款地址(pay_url)
"""


def pay(alipay, address_id, pdduid, accesstoken, sku_id, group_id, goods_id):
    url = 'https://api.pinduoduo.com/order?pdduid={}'.format(pdduid)
    headers['Referer'] = 'https://mobile.yangkeduo.com/order_checkout.html?sku_id={}&group_id={}&goods_id={}&' \
                         'goods_number=1'.format(sku_id, group_id, goods_id)
    headers['accesstoken'] = accesstoken
    json_str = {
        "address_id": address_id,
        "goods": [{"sku_id": sku_id, "sku_number": 1, "goods_id": goods_id}],
        "group_id": group_id,
        "duoduo_type": 0,
        "biz_type": 0,
        "source_channel": -1,
        "source_type": 0,
        "app_id": 9,
        "is_app": "0",
        "version": 1
    }

    # 循环请求，3次请求仍获取不到，则判断token失效
    order_sn = ''
    for i in range(3):
        time.sleep(random.random())
        res = requests.post(url, headers=headers, json=json_str, verify=False)
        res_json = res.json()
        if 'order_sn' in res_json:
            order_sn = res_json['order_sn']
            break
        elif 'error_code' in res_json and i == 2:
            return False, 'access_token错误, 请更新.'
        else:
            print('重试第{}次'.format(i + 1))
            continue
    print('订单编号: {}'.format(order_sn))

    if alipay:
        print('支付宝支付...')
        url2 = 'https://api.pinduoduo.com/order/prepay?pdduid={}'.format(pdduid)
        t_data = {
            "order_sn": order_sn,
            "app_id": 9,
            "return_url": "https://mobile.yangkeduo.com/alipay_callback.html?order_sn={}".format(order_sn),
            "version": 2,
            "attribute_fields": {"paid_times": 0}
        }
        res2 = requests.post(url2, headers=headers, verify=False, json=t_data)
        xiadan_json = res2.json()
        gateway_url = xiadan_json['gateway_url']
        query = xiadan_json['query']
        a = urllib.parse.urlencode(query)
        dingdan_url = gateway_url + '?' + a
        response = requests.get(dingdan_url, headers=headers, verify=False)
        pay_url = response.url
    else:
        print('微信支付...')
        url2 = 'https://api.pinduoduo.com/order/prepay?pdduid={}'.format(pdduid)
        t_data = {
            "order_sn": order_sn,
            "app_id": 38,
            "pap_pay": 1,
            "version": 1,
            # "attribute_fields": {"paid_times": 0}
        }
        res = requests.post(url2, headers=headers, verify=False, json=t_data)
        xiadan_json = res.json()
        nweb_url = xiadan_json['mweb_url']
        headers['Referer'] = 'https://mobile.yangkeduo.com/wechat_h5_pay_callback.html?order_sn={}'.format(order_sn)
        res2 = requests.get(nweb_url, headers=headers, verify=False)
        pay_url = re.findall('var url="(.*?)";', res2.text, re.I | re.S)[0]
    return order_sn, pay_url


# 获取增加收货地址
def get_shipping_address(pdduid, accesstoken):
    addresses_url = 'https://api.pinduoduo.com/addresses?pdduid={}'.format(pdduid)
    headers['accesstoken'] = accesstoken
    response = requests.get(addresses_url, headers=headers, verify=False)
    if len(response.json()) == 0:
        url = 'https://api.pinduoduo.com/address?pdduid={}'.format(pdduid)
        add_data = {
            "address": "32栋",
            "city_id": 76,
            "district_id": 693,
            "mobile": "15179833221",
            "name": "zs",
            "province_id": 6
        }
        add_response = requests.post(url, headers=headers, json=add_data, verify=False)
        if 'server_time' in add_response.json():
            print('新增收货地址成功')
            return True, '新增收货地址成功'
        else:
            print('新增收货地址失败')
            return False, '新增收货地址失败'
    else:
        if 'error_code' in response.json():
            print('access_token错误，请更新.')
            return False, 'access_token错误，请更新.'
        print('已存在收货地址')
        return True, '已存在收货地址'


def main(pdduid, accesstoken, goods_url):
    # TODO goods_url, accesstoken, pdduid
    # 是否支付宝支付， True为是
    alipay = False
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)

    """判断收货地址，没有则增加"""
    is_add, msg = get_shipping_address(pdduid, accesstoken)
    if is_add is False:
        return {'code': 0, 'pay_url': '', 'order_sn': '', 'error_msg': msg}

    """获取商品信息"""
    sku_id, group_id, goods_id = get_goods_id(goods_url, cookie)

    """获取地区ID"""
    address_id = get_address_id(sku_id, group_id, goods_id)
    if '错误' not in address_id:
        order_sn, pay_url = pay(alipay, address_id, pdduid, accesstoken, sku_id, group_id, goods_id)
        print('付款链接: {}'.format(pay_url))
        if '错误' in pay_url:
            return {'code': 0, 'pay_url': '', 'order_sn': '', 'error_msg': pay_url}
        logger.log('INFO', '支付链接返回正常', 'spider', pdduid)
        return {'code': 1, 'pay_url': pay_url, 'order_sn': order_sn, 'error_msg': ''}
    else:
        logger.log('ERROR', '未获取到地区ID, 更新accesstoken后重试', 'spider', pdduid)
        print('程序结束, 未获取到地区ID, 更新accesstoken后重试...')
        return {'code': 0, 'pay_url': '', 'order_sn': '', 'error_msg': address_id}


if __name__ == '__main__':
    goods_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=9962830&is_spike=0&page_el_sn=99862&refer_page_name=index&refer_page_id=10002_1534904453632_CTDgPWCMNe&refer_page_sn=10002&refer_page_el_sn=99862'
    pdduid = 18443241194
    accesstoken = '7MET6NIDCXKZHRWLOUSQBSKPSK7JE6RT5U7VRPEY77WODRFLSQQQ10264ae'
    main(pdduid, accesstoken, goods_url)
