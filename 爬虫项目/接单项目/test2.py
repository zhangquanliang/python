# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
import json

# 验证码识别工具
def ocr_verify_code(file_path):
    try:
        # 要上传到打码平台的数据
        api_username = "yzdama"
        api_password = "p@ssw)rd12345"
        api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
        yzm_min = ''
        yzm_max = ''
        yzm_type = ''
        tools_token = ''
        data = {"user_name": '%s' % api_username,
                "user_pw": "%s" % api_password,
                "yzm_minlen": "%s" % yzm_min,
                "yzm_maxlen": "%s" % yzm_max,
                "yzmtype_mark": "%s" % yzm_type,
                "zztool_token": "%s" % tools_token,
                }

        files = {
            'upload': (file_path, open(file_path, 'rb'), 'image/png')
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.1,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/1.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Connection': 'keep-alive',
            'Host': 'v1-http-api.jsdama.com',
            'Upgrade-Insecure-Requests': '1'
        }
        # 实例化连接对象
        s = requests.session()
        result = s.post(api_post_url, headers=headers, data=data, files=files, verify=False)
        # 返回数据
        result = result.text
        res = json.loads(result)
        if res['result']:
            return res['data']['val']
    except Exception as e:
        print('验证码识别错误,错误信息为===>', e)

ocr_verify_code()