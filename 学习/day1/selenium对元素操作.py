# -*- coding: utf-8 -*-
# 对元素进行简单操作

from selenium import webdriver
import time, datetime
# driver = webdriver.Ie()
# driver.get("https://login.taobao.com")
# driver.find_element_by_id('J_Quick2Static').click()
# # 文本输入框
# driver.find_element_by_id("TPL_username_1").clear()   # 清除文本输入框数据
# driver.find_element_by_id('TPL_username_1').send_keys('heidlzzhan')  # send_keys对文本框输入值
# time.sleep(1)
#
# driver.find_element_by_id("TPL_password_1").clear()   # 清除文本输入框数据
# driver.find_element_by_id('TPL_password_1').send_keys('ZQL131415..')
#
# driver.find_element_by_id('J_SubmitStatic').click()

from selenium.webdriver.common.keys import Keys

driver = webdriver.Ie()
driver.get("http://www.baidu.com")

# 输入框输入内容
elem = driver.find_element_by_id("kw")
elem.send_keys("Eastmount CSDN")
time.sleep(3)

# 删除一个字符CSDN 回退键
elem.send_keys(Keys.BACK_SPACE)
elem.send_keys(Keys.BACK_SPACE)
elem.send_keys(Keys.BACK_SPACE)
elem.send_keys(Keys.BACK_SPACE)
time.sleep(3)

# 输入空格+"博客"
elem.send_keys(Keys.SPACE)
elem.send_keys(u"博客")
time.sleep(3)

# ctrl+a 全选输入框内容
elem.send_keys(Keys.CONTROL, 'a')
time.sleep(3)

# ctrl+x 剪切输入框内容
elem.send_keys(Keys.CONTROL, 'x')
time.sleep(3)

# 输入框重新输入搜索
elem.send_keys(Keys.CONTROL, 'v')
time.sleep(3)

# 通过回车键替代点击操作
driver.find_element_by_id("su").send_keys(Keys.ENTER)
time.sleep(3)

driver.quit()