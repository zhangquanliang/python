# 引入需要的模块
import ctypes
import datetime
import json
import time

import requests
from PIL import Image
from pykeyboard import PyKeyboard

k = PyKeyboard()


class Tools():
    def __init__(self):
        return

    # 通用request工具
    @staticmethod
    def request_tools(url, headers=None, cookies=None, proxies=None, params=None, timeout=20, datas=None, json_data=None, type="get"):
        # 初始化连接对象
        s = requests.session()
        # 设置返回值参数
        ret = {"issuccess": 0, "content": "", "text": "", "cookies": "",
               "json": ""}  # issuccess 访问是否成功； content 网页源码; cookies 保存网页cookie.
        try:
            # 判断各参数是否有效，并设置参数
            # 访问头部信息
            if headers is not None:
                s.headers = headers
            # cookie信息
            if cookies is not None:
                s.cookies = cookies
            # 代理信息
            if proxies is not None:
                s.proxies = proxies
            # post请求参数信息
            if params is not None:
                s.params = params
            # 访问超时设置
            if timeout != 20:
                s.timeout = timeout
            # post方式访问
            if type is not "get":
                r = s.post(url, data=datas, json=json_data, verify=False)  # verify=False可以屏蔽掉网站证书验证
                # 判断访问成功后设置返回值参数
                if r:
                    ret["issuccess"] = 1
                    ret["content"] = r.content
                    ret["text"] = r.text
                    ret["cookies"] = s.cookies
            # get方式访问
            else:
                r = s.get(url, verify=False)

                if r:
                    ret["issuccess"] = 1
                    ret["content"] = r.content
                    ret["text"] = r.text
                    ret["cookies"] = s.cookies
        # 捕获异常
        except Exception as e:
            print(e)
        # 关闭连接
        finally:
            if s:
                s.close()
        # 返回数据
        return ret

    # 截取验证码并发送打码平台识别
    @staticmethod
    def cut_verify_code(driver, img_path, new_img_path, *args):
        driver.get_screenshot_as_file(img_path)
        img = Image.open(img_path)
        region = img.crop(args)
        path = new_img_path
        region.save(path)

    # 验证码识别工具
    @staticmethod
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
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
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

    # 读取cookies
    @staticmethod
    def read_cookie():
        try:
            with open('../../tests/cookies.json', 'r') as f:
                cookie = f.read()
                return cookie
        except Exception as e:
            print("处理cookie异常是===>", e)

    # 字符串类型日期转为日期类型日期，参数为字符串日期和日期格式，精确到年月日的格式为："%Y-%m-%d"，精确到时分秒的格式为"%Y-%m-%d %H:%M:%S"
    @staticmethod
    def date_format_transform(date, date_format):
        date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, date_format)))
        return date

        # 调用硬件模拟输入的dll，用于输入安全控件的密码

    @staticmethod
    def key_send(string):
        key_call_dll = ctypes.cdll.LoadLibrary(r'..\..\util\KeyCall.dll')
        # 某些情况下（民生银行安全控件输入密码），KeySendChar输入多个字符时会丢失（实际输入少于字符串长度），所以这里改为逐个输入
        for c in string:
            try:
                key_call_dll.KeySendChar(c)
                time.sleep(0.5)
            except Exception as ex:
                pass
                # 即使正常输入，KeySendChar还是会报异常，所以这里将异常捕获不进行任何处理
                # ignore_error = ex.message
                # print(ignore_error)
                # print(ex)
        return

    @staticmethod
    def send_enter():
        k.press_key(k.enter_key)
        k.release_key(k.end_key)

    @staticmethod
    def send_tab():
        k.press_key(k.tab_key)
        k.release_key(k.tab_key)


def send_enter():
    k.press_key(k.enter_key)
    k.release_key(k.end_key)


def send_tab():
    k.press_key(k.tab_key)
    k.release_key(k.tab_key)


def send_space():
    k.press_key(k.space_key)
    k.release_key(k.space_key)


# 软件模拟，控件环境下不行
def send_keys(string):
    assert isinstance(string, str)
    k.type_string(string)
