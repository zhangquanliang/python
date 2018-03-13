#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

path = r"D:\Git\MyProject\zhangql\resources\chromedriver.exe"
driver=webdriver.Chrome(executable_path=path)
try:
    driver.implicitly_wait(30)
    driver.get('http://net.chinamobile.com/ucas/login?service=http%3A%2F%2Fnet.chinamobile.com%3A80%2Fcmccnkms-case%2Fj_acegi_cas_security_check%3Bjsessionid%3D605E4CD20B2FBD68D5DE968973B78EDE%3Ft%3Dhttp%253A%252F%252Fnet.chinamobile.com%252Fcmccnkms-case%252Fweb%252FkmIndex%252FtoKmIndex.action')
    driver.find_element_by_id("passWord_1").clear()
    driver.find_element_by_id("passWord_1").send_keys("123356")
    mouse = driver.find_element_by_css_selector('input.login-btnhover')
    ActionChains(driver).move_to_element(mouse).perform()
    checkboxes = driver.find_element_by_css_selector("input.login-btnhover").send_keys(Keys.ENTER)

finally:
    print("success")
