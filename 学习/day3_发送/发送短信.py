# -*- coding:utf-8 -*-
from collections import Counter

from twilio.rest import Client

def send_sms(my_number=None):
    # 从官网获得以下信息
    account_sid = 'AC73cd1296027b9a3179878efffd346df9'
    auth_token = 'd29aaff33d77cce1c311ec62a7b43f62'
    twilio_number = '+1 681 433 8240'

    client = Client(account_sid, auth_token)
    b = client.calls.get(account_sid)
    msg = '你好，我是来自于twilio的短信，请联系我.'.encode('utf-8')
    try:
        message = client.messages.create(to=my_number, from_=twilio_number, body=msg)
        print(message.sid)
        print('短信已经发送！')
    except ConnectionError as e:
        print('发送失败，请检查你的账号是否有效或网络是否良好！')
        return e


send_sms(my_number='+8615179833772')