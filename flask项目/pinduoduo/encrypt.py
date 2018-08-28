# -*- coding:utf-8 -*-
__author__ = '张全亮'
import re
import base64
import hashlib

# 控制台参数加密函数（一般用不上，脚本端只负责解密），加密逻辑：先进行一次base64编码，再进行字符串反转，最后进行第二次base64编码
def param_encode(param_str):
    temp_bytes = bytes(str(param_str), encoding='utf-8')
    temp_bytes = base64.b64encode(temp_bytes)  # 第一次base64解码
    temp_str = str(temp_bytes, encoding='utf-8')
    temp_list = list(temp_str)
    temp_list.reverse()  # 字符串反转
    temp_str = ''.join(temp_list)
    temp_bytes = bytes(temp_str, encoding='utf-8')
    temp_bytes = base64.b64encode(temp_bytes)  # 第二次base64解码
    temp_str = str(temp_bytes, encoding='utf-8')
    return temp_str


# 控制台参数解密函数，解密逻辑：先进行一次base64解码，再进行字符串反转，最后进行第二次base64解码
def param_decode(encrypt_str):
    temp_bytes = bytes(encrypt_str, encoding='utf-8')
    temp_bytes = base64.b64decode(temp_bytes)  # 第一次base64解码
    temp_str = str(temp_bytes, encoding='utf-8')
    temp_list = list(temp_str)
    temp_list.reverse()  # 字符串反转
    temp_str = ''.join(temp_list)
    temp_bytes = bytes(temp_str, encoding='utf-8')
    temp_bytes = base64.b64decode(temp_bytes)  # 第二次base64解码
    temp_str = str(temp_bytes, encoding='utf-8')
    return temp_str


# 生成MD5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))

    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + hl.hexdigest())


import pdd_spider
with open('账号.txt', 'r', encoding='utf8') as f:
    for line in f.readlines():
        a = re.findall('卡号：(\d+).密码：.(.*?)加密：(\d+)', line)
        if len(a) == 0:
            continue
        print('写入', genearteMD5(str(a)))
        # param_str = a[0][0] + '<zhangql>' + a[0][1] + '<zhangql>' + a[0][2]
        # url = 'http://192.168.2.152:80/api/pay'
        # import requests
        #
        # goods_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=9962830&is_spike=0&page_el_sn=99862&refer_page_name=index&refer_page_id=10002_1534904453632_CTDgPWCMNe&refer_page_sn=10002&refer_page_el_sn=99862'
        # data = {
        #     'pdduid': a[0][0],
        #     'accesstoken': a[0][1],
        #     'goods_url': goods_url
        # }
        # result = requests.post(url, data=data)
        # print(result.json())
        # encode = param_encode(param_str)
        # with open('加密后文件.txt', 'a+', encoding='utf8') as f2:
        #     f2.write(encode + '\n')
        # print('加密后', encode)
        # print('解密后', param_decode(encode))