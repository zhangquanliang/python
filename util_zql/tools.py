# 引入需要的模块
import ctypes
import datetime
import json
import time

import requests
from PIL import Image
from pykeyboard import PyKeyboard
import win32com.client

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
        import os
        absolute_path = os.path.dirname(__file__)
        key_call_dll = ctypes.cdll.LoadLibrary(os.path.join(absolute_path, 'KeyCall.dll'))
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


# class AutoIt():
#
#     """
#     title：标题。一般是用窗口的标题来做识别的（"无标题"）。也可以用class（[CLASS:class]）。
#     官方文档：https://www.autoitscript.com/autoit3/docs/intro/windowsadvanced.htm
#     A special description can be used as the window title parameter. This description can be used to identify a window by the following properties:
#         TITLE - Window title
#         CLASS - The internal window classname
#         REGEXPTITLE - Window title using a regular expression (if the regular expression is wrong @error will be set to 2)
#         REGEXPCLASS - Window classname using a regular expression (if the regular expression is wrong @error will be set to 2)
#         LAST - Last window used in a previous Windows AutoIt Function (see Windows Management Functions)
#         ACTIVE - Currently active window
#         X \ Y \ W \ H - The position and size of a window
#         INSTANCE - The 1-based instance when all given properties match
#
#     control_id：控件的标识符。通用格式：[CLASS:class;TEXT:text;INSTANCE:2]。
#     官方文档：https://www.autoitscript.com/autoit3/docs/intro/controls.htm
#     A special description can be used as the controlID parameter used in most of the Control...() functions. This description can be used to identify a control by the following properties:
#         ID - The internal control ID. The Control ID is the internal numeric identifier that windows gives to each control. It is generally the best method of identifying controls. In addition to the AutoIt Window Info Tool, other applications such as screen readers for the blind and Microsoft tools/APIs may allow you to get this Control ID
#         TEXT - The text on a control, for example "&Next" on a button
#         CLASS - The internal control classname such as "Edit" or "Button"
#         CLASSNN - The ClassnameNN value as used in previous versions of AutoIt, such as "Edit1"
#         NAME - The internal .NET Framework WinForms name (if available)
#         REGEXPCLASS - Control classname using a regular expression
#         X \ Y \ W \ H - The position and size of a control.
#         INSTANCE - The 1-based instance when all given properties match.
#     """
#     auto_it = win32com.client.Dispatch("AutoItX3.Control")
#
#     @classmethod
#     def exc_fun(cls, fun_name, *args):
#         fun = getattr(cls.auto_it, fun_name)
#         return fun(*args)
#
#     @classmethod
#     def win_wait(cls, title, text='', timeout=0):
#         return cls.auto_it.WinWait(title, text, timeout)
#
#     @classmethod
#     def win_close(cls, title):
#         return cls.auto_it.WinClose(title)
#
#     @classmethod
#     def win_exists(cls, title):
#         return cls.WinExists(title)
#
#     @classmethod
#     def win_activate(cls, title):
#         return cls.auto_it.WinActivate(title)
#
#     @classmethod
#     def win_set_top(cls, title):
#         return cls.auto_it.WinSetOnTop(title)
#
#     @classmethod
#     def win_get_text(cls, title, text=''):
#         win_text = cls.auto_it.WinGetText(title, text)
#         return str(win_text)
#
#     @classmethod
#     def win_get_position(cls, title, text=''):
#         return cls.auto_it.WinGetPosX(title, text), cls.auto_it.WinGetPosY(title, text)
#
#     @classmethod
#     # flag:0取消置顶，1置顶
#     def win_set_on_top(cls, title, text='', flag=1):
#         return cls.auto_it.WinSetOnTop(title, text, flag)
#
#     @classmethod
#     def win_set_state(cls, title, text='', flag=3):
#         return cls.auto_it.WinSetState(title, text, flag)
#
#     @classmethod
#     def control_click(cls, title, text, control_id, button='left', clicks='1'):
#         return cls.auto_it.ControlClick(title, text, control_id, button, clicks)
#
#     @classmethod
#     def control_set_text(cls, title, text, control_id, new_text, flag=0):
#         return cls.auto_it.ControlSetText(title, text, control_id, new_text, flag)
#
#     @classmethod
#     def control_focus(cls, title, text, control_id):
#         return cls.auto_it.ControlFocus(title, text, control_id)
#
#     @classmethod
#     def control_get_position(cls, title, text, control_id):
#         return cls.auto_it.ControlGetPosX(title, text, control_id), cls.auto_it.ControlGetPosY(title, text, control_id)


if __name__ == '__main__':
    pass
    # a = AutoIt.exc_fun('WinWait', 'Everything', '', '5')
    # print(a)



