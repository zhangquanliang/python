# coding=utf-8
import time
import sys

from selenium import webdriver
import pymouse
import pykeyboard
import urllib3
from PIL import Image

from common.common_tool import console_param_handle, console_result_handle
from util.tools import Tools
from model.models import LoginAcc, ConsoleResult

urllib3.disable_warnings()  # 屏蔽http警告

try_time = 1  # 尝试次数


# 模拟用户登录
def login(username, operator_number, password):
    global try_time

    # 实例化鼠标和键盘模拟对象
    m = pymouse.PyMouse()
    k = pykeyboard.PyKeyboard()
    driver = webdriver.Ie(executable_path=r'D:\C Git\D project\zhangql\util_zql\IEDriverServer(zql).exe')
    start_url = 'https://ebank.hzbank.com.cn/custody/'
    driver.get(start_url)
    driver.maximize_window()
    time.sleep(3)

    # 截取验证码
    driver.get_screenshot_as_file('hzb_screen_shot.png')
    img = Image.open('hzb_screen_shot.png')
    region = img.crop((1094, 391, 1198, 427))  # 本地
    # region = img.crop((952, 297, 1033, 320))  # 生产机
    path = 'hzb_verify_code.png'
    region.save(path)
    # 发送到打码平台获取验证码
    verify_code = Tools.ocr_verify_code(path)

    # 输入用户名
    elem = driver.find_element_by_xpath('//input[@ng-model="customerId"]')
    elem.clear()
    elem.send_keys(username)
    time.sleep(1)

    # 输入操作员号
    # elem = driver.find_element_by_xpath('//input[@ng-model="operId"]')
    k.press_key(k.tab_key)  # 点tab键可以直接切换
    k.release_key(k.tab_key)
    k.type_string(operator_number)
    time.sleep(1)

    # 输入密码
    m.click(1030, 406)
    Tools.key_send(password)
    time.sleep(1)

    # 输入验证码
    elem = driver.find_element_by_xpath('//*[@ng-model="verifyCode"]')
    elem.clear()
    elem.send_keys(verify_code)
    time.sleep(1)

    # 点击登录
    elem = driver.find_element_by_xpath('//*[@ng-click="loginSubmit()"]')
    elem.click()
    time.sleep(8)  # 等待网页加载完全

    try:
        # 获取弹窗警告内容
        alert = driver.switch_to.alert.text
        time.sleep(1)
        # 获取警告对话框的内容
        if alert:
            print("获取到的弹窗内容为", alert.text)
            time.sleep(1)
            if alert.text == '请输入客户号!' or '客户号输入有误,请输入数字!':
                if try_time <= 2:
                    try_time += 1
                    login(username, operator_number, password)
                if try_time > 2:
                    result = ConsoleResult(success=False, code=1001, data={}, error_data={}, error='').to_dict()
                    return result
            elif alert.text == '操作员号输入有误！请输入长度4位的数字！' or alert.text == '交易失败： 操作员数据未找到(-77074)':
                if try_time <= 2:
                    try_time += 1
                    login(username, operator_number, password)
                if try_time > 2:
                    result = ConsoleResult(success=False, code=1001, data={}, error_data={}, error='').to_dict()
                    return result
            elif alert.text == '交易失败： 用户名或密码错(-77056)':
                result = ConsoleResult(success=False, code=1003, data={}, error_data={}, error='').to_dict()
                return result
            elif alert.text == '验证码输入有误！':
                if try_time <= 2:
                    try_time += 1
                    login(username, operator_number, password)
                if try_time > 2:
                    result = ConsoleResult(success=False, code=1004, data={}, error_data={}, error='').to_dict()
                    return result
    except Exception as ex:
        print('异常信息是:', ex)

    cookies = driver.get_cookies()
    login_infos = LoginAcc()
    cookie_list = []

    # 获取cookie
    str_cookie = ""
    cookie_dict = cookies[6]
    str_cookie = cookie_dict['name'] + '=' + cookie_dict['value']

    # 获取session_token
    session_token_dict = cookies[4]
    session_token = session_token_dict['value']

    login_infos.login_user = username
    login_infos.cookie = str_cookie
    login_infos.authorization_extend1 = session_token

    result = ConsoleResult(success=True, code=0, data=login_infos.to_dict(), error_data={}, error='').to_dict()
    print(result)
    driver.quit()
    return result

def run():
    console_result = login(username='999900323', operator_number='2002', password='639196')


def main():
    params = sys.argv
    json_param = console_param_handle(params)
    # 对参数进行校验
    if "login_user" not in json_param.keys() or "login_password" not in json_param.keys():
        console_result = {
            "success": False,
            "data": {},
            "code": 100,  # 参数错误的错误码统一为 100
            "error": "参数错误！({})".format(params)
        }
    else:
        # 参数正确，调用主方法，获取结果
        operator_number = None if 'operator_number' not in json_param.keys() else json_param['operator_number']
        console_result = login(username=json_param['login_user'], operator_number=json_param['login_extend1'],
                               password=json_param['login_password'])
    print(console_result_handle(console_result))  # 将最终结果输出


if __name__ == '__main__':
    run()
    # main()
