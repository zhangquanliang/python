# -*- coding: utf-8 -*-
import sys
import time
import win32api
import win32con
import re
import urllib3
urllib3.disable_warnings()

import pymouse
import pykeyboard
from PIL import Image
from selenium import webdriver
import requests

from util import tools
from util.tools import Tools
from bank.cmbe.find_root_path import FindRootPath
from common.common_tool import console_result_handle, console_param_handle
FindRootPath.find()
err_i = 0


# 南京银行登录方法
def login(login_user, login_password, mcrypt_key=None, password_encrypted=None):
    image_path = './images/NJ_verify_code.png'
    login_url = 'https://ebank.njcb.com.cn/corporbank/public/login.jsp'
    emp_sid = ""

    if mcrypt_key is None or password_encrypted is None:
        key = pykeyboard.PyKeyboard()
        mouse = pymouse.PyMouse()

        driver = webdriver.Ie(executable_path=r'..\..\util\IEDriverServer.exe')
        driver.maximize_window()
        driver.get(url=login_url)

        # 点击元素ID为verifyCodeImg的位置
        driver.find_element_by_id('verifyCodeImg').click()

        # 验证码xpath地址
        image_location = '//*[@id="verifyCodeImg"]'
        driver.save_screenshot(image_path)
        im = Image.open(image_path)

        left = driver.find_element_by_xpath(image_location).location['x']
        top = driver.find_element_by_xpath(image_location).location['y']
        right = left + driver.find_element_by_xpath(image_location).size['width']
        bottom = top + driver.find_element_by_xpath(image_location).size['height']
        im = im.crop((left, top, right, bottom))
        im.save(image_path)

        verify_code = tools.Tools.ocr_verify_code(image_path)  # 验证码识别

        # 填写用户名
        driver.find_element_by_id('customerId').click()
        time.sleep(0.5)
        win32api.keybd_event(17, 0, 0, 0)  # ctrl建
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        key.type_string(login_user)
        time.sleep(0.5)

        # 填写密码
        mouse.click(980, 313, 1, 2)
        time.sleep(0.5)
        Tools.key_send(login_password)

        # 填写验证码
        driver.find_element_by_id('verifyCode').click()
        key.type_string(verify_code)
        time.sleep(0.5)

        # 登录按钮
        driver.find_element_by_id('btn_login').click()

        global err_i
        for i in range(3):
            time.sleep(10)

            try:
                # 获取登录错误信息，登录成功抛出异常
                err_text = driver.find_element_by_xpath('/HTML/BODY/DIV[6]/DIV[1]').text
                if err_text.find('未找到该客户') > -1:
                    driver.quit()
                    result = {"success": False, "data": {}, "code": 1001, "error": err_text}
                    return result
                if err_text.find('请输入正确的验证码') > -1 or err_text.find('超时'):
                    err_i += 1
                    print(u'验证码错误，正在尝试第%s次重新登录' % err_i)
                    if err_i == 3:
                        print(u'验证码识别%s次错误，停止重新登录' % err_i)
                        result = {"success": False, "data": {}, "code": 1005, "error": err_text}
                        driver.quit()
                        return result
                    driver.quit()
                    time.sleep(3)
                    return login(login_user, login_password)
            except Exception as e:
                pass

            html = driver.page_source
            # 正则提取所需要的参数emp_sid
            reg = re.findall('<INPUT type=hidden value=(.*?) name=EMP_SID>', html)
            emp_sid = reg[0]
            break

        cookies = driver.get_cookies()
        cookie = ""
        for cookie_ in cookies:
            cookie = "%s;%s=%s" % (cookie, cookie_["name"], cookie_["value"])
        driver.quit()

    else:
        r = requests.session()
        r.get(login_url, verify=False)

        code_url = 'https://ebank.njcb.com.cn/corporbank/public/VerifyImage?update=0.027584966143414602'
        response = r.get(code_url, verify=False)

        f = open('./images/NJ_verify_code.png', 'wb')
        f.write(response.content)
        f.close()

        verify_code = tools.Tools.ocr_verify_code('./images/NJ_verify_code.png')  # 验证码识别

        post_login_url = 'https://ebank.njcb.com.cn/corporbank/publicLogin.do'
        data = {
            "checkCode": verify_code,
            "customerId": login_user,
            "inputType": "2",
            "netType": "1"
        }

        cookie_dit = r.cookies.get_dict()
        cookie = ""
        for key, value in cookie_dit.items():
            cookie = "%s;%s=%s" % (cookie, key, value)

        response = r.post(post_login_url, data=data, verify=False)
        html = response.text
        if html.find(u'未找到该客户账户') > -1:
            print(u'未找到该客户账户[{}]信息,请核实'.format(login_user))
            result = {
                "success": False,
                "data": {},
                "code": 1001,
                "error": '登录账户错误'
            }
            return result

        reg = re.findall(r'EMP_SID=(.*?)\|null', html)
        emp_sid = reg[0]

    if cookie:
        result = {
            "success": True,
            "data": {"cookie": cookie, "emp_sid": emp_sid, "mcrypt_key": '1', },
            "code": 0,
            "error": ""
        }
    else:
        result = {
            "success": False,
            "data": {},
            "code": -101,
            "error": "Cookie获取失败"
        }

    return result


def test():
    print('test..')
    console_result = login(login_user='05060124770000535', login_password='888888', mcrypt_key='1', password_encrypted='1')
    print(console_result)


def main():
    # 入参格式：json_param = sys.argv[1]. sys.argv[0]是当前脚本文件。参数为json格式。
    # 例：{'login_user':'05060124770000535','login_password':'888888'}
    params = sys.argv
    # 参数处理
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
        console_result = login(login_user=json_param['login_user'], login_password=json_param['login_password'])
    print(console_result_handle(console_result))  # 将最终结果输出


if __name__ == "__main__":
    main()
    # test()