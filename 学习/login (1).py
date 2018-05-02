# -*- coding: utf-8 -*-
import urllib3
import ssl
import re
import sys
import time
import pykeyboard
import pymouse

from model.models import ErrorInfo, ConsoleResult
from util.tools import Tools

from selenium import webdriver
location_postiton=(1047,395)
from common.common_tool import console_result_handle, console_param_handle
mouse=pymouse.PyMouse()
key = pykeyboard.PyKeyboard()
ssl._create_default_https_context = ssl._create_unverified_context
# 屏蔽http警告
from multiprocessing import Pool
urllib3.disable_warnings()
try_time = 0 # 重试次数
# 登陆
def login(password):
    global try_time
    login_info = {}
    pool = Pool(processes=2)
    login_url = "https://corporbank.bsb.com.cn/corporbank/logon.jsp"
    driver=webdriver.Ie(executable_path=r'D:\C Git\D project\huarun\util\IEDriverServer.exe')
    pool.apply_async(choose_certificate)
    driver.get(login_url)
    driver.maximize_window()
    pool.close()
    pool.join()
    time.sleep(2)

    fill_form(password)
    time.sleep(3)
    html=driver.page_source
    if '密码验证失败' in html:
     if try_time>1:
         error_data = ErrorInfo(acc_number=-1, error_msg='登录异常')
         result = ConsoleResult(success=False, code=1001, data={}, error_data=error_data.to_dict(), error='').to_dict()
         return result
     else:
         try_time+=1
         result=login(password)
         return result

    else:
        cookies = driver.get_cookies()
        str_cookie = ""
        for cookie in cookies:
            str_cookie = "%s;%s=%s" % (str_cookie, cookie["name"], cookie["value"])
        page_source = driver.page_source  # 获
        # 取网页源代码
        time.sleep(10)
        pattern = re.compile(r'.*EMP_SID=(.*)"')
        match = pattern.search(page_source)
        emp_sid = ""
        if match:
            emp_sid = match.group(1)
        login_info["authorization_cookie"] = str_cookie
        login_info["authorization_extend1"] = emp_sid
        return driver


# 确定证书
def choose_certificate():
    time.sleep(4)
    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(0.5)
    key.press_key(key.enter_key)
    key.release_key(key.enter_key)
    time.sleep(2)


def fill_form(password):
    time.sleep(5)
    Tools.key_send(password)
    time.sleep(1)

    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(0.5)

    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(0.5)

    key.press_key(key.enter_key)
    key.release_key(key.enter_key)
    time.sleep(1)

    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(1)

    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(1)
    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(1)
    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(1)
    key.press_key(key.tab_key)
    key.release_key(key.tab_key)
    time.sleep(1)

    key.press_key(key.shift_key)
    key.release_key(key.shift_key)
    Tools.key_send(password)
    time.sleep(1)

    key.press_key(key.enter_key)
    key.release_key(key.enter_key)
    time.sleep(1)
    # print('aa')








def main():
    # 入参格式：json_param = sys.argv[1]. sys.argv[0]是当前脚本文件。参数为json格式。
    # 例：{'cookie':'ead121212','acc_number':'2191919','data':{'a':'b'}}
    params = sys.argv
    # 参数处理
    json_param = console_param_handle(params)
    # 对参数进行校验
    if  "password" not in json_param.keys():
        console_result = {
            "success": False,
            "data": {},
            "code": 100,  # 参数错误的错误码统一为 100
            "error": "参数错误！({})".format(params)
        }
    else:
        # 参数正确，调用主方法，获取结果
        console_result = login(password=json_param['password'])
    print(console_result_handle(console_result))  # 将最终结果输出


def test():
    console_result = login("Qw33031933")
    print(console_result)


if __name__ == '__main__':
    test()

    # main()

