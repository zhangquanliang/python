# -*-coding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time, re, random, os, base64, cv2
import numpy as np


class CrackGeetest():
    def __init__(self):
        self.url = 'https://passport.jd.com/new/login.aspx'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

    def mk_img_dir(self):
        """
        创建图片目录文件
        :return:
        """
        if not os.path.exists('Image'):
            os.mkdir('Image')

    def get_geetest_image(self):

        """
        获取验证码图片
        :return: 图片location信息
        """
        error_user = '123'
        error_passwd = 123
        self.browser.get(self.url)
        user_login = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[3]/a')))
        user_login.click()
        input_user = self.browser.find_element_by_xpath('//input[@id="loginname"]')
        input_passwd = self.browser.find_element_by_xpath('//input[@type="password"]')
        login_submit = self.browser.find_element_by_xpath('//a[@id="loginsubmit"]')
        for i in range(2):
            input_user.clear()
            input_user.send_keys(error_user)
            input_passwd.clear()
            input_passwd.send_keys(error_passwd)
            login_submit.click()
            time.sleep(0.5)
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="authcode-btn"]')))
        button.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="JDJRV-bigimg"]/img')))
        time.sleep(0.5)
        template_url = self.browser.find_element_by_xpath('//div[@class="JDJRV-bigimg"]/img').get_attribute('src')
        time.sleep(0.5)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="JDJRV-smallimg"]/img')))
        target_url = self.browser.find_element_by_xpath('//div[@class="JDJRV-smallimg"]/img').get_attribute('src')
        template_img = re.findall('base64,(.*)', template_url, re.S)[0]
        target_img = re.findall('base64,(.*)', target_url, re.S)[0]
        with open('template.jpg', 'wb') as f:
            f.write(base64.b64decode(template_img))
            print('缺口图片下载完成！')
        with open('target.jpg', 'wb') as f:
            f.write(base64.b64decode(target_img))
            print('目标图片下载完成！')

    # def show(self, name):
    #     #显示识别出缺口的图片
    #     cv2.imshow('Show', name)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    def get_grap(self):
        otemp = 'target.jpg'
        oblk = 'template.jpg'
        target = cv2.imread(otemp, 0)
        template = cv2.imread(oblk, 0)
        w, h = target.shape[::-1]
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        y, x = np.unravel_index(result.argmax(), result.shape)
        # 展示圈出来的区域
        # cv2.rectangle(template, (x, y), (x + w, y + h), (7, 249, 151), 2)
        # self.show(template)
        print('缺口偏移量：', x)

        return x

    def get_track(self, distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                a = random.uniform(3, 5)
            else:
                a = -(random.uniform(10, 11))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.8
                tracks.append(round(x, 2))
            elif 1 < current - distance < 1.5:
                x = x - 1.25
                tracks.append(round(x, 2))
            elif 1.5 < current - distance < 2:
                x = x - 1.75
                tracks.append(round(x, 2))
            elif 2 < current - distance < 3:
                x = x - 2.5
                tracks.append(round(x, 2))
            else:
                tracks.append(round(x, 2))

        back_tracks=[]
        for i in range(10):
             back_tracks.append(random.randint(-5,0))
        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': tracks, 'back_tracks': back_tracks}
       # return tracks

    def get_slider(self):
        """
        获取滑块
        :return:滑块对象
        """
        try:
            slider = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="slideAuthCode"]/div/div[2]/div[3]')))
            return slider
        except TimeoutError:
            print('加载超时...')

    def move_to_gap(self, slider, tracks, distance):
        """
        将滑块移动至偏移量处
        :param slider: 滑块
        :param tracks: 移动轨迹
        :return:
        """


        ActionChains(self.browser).click_and_hold(slider).perform()
        time.sleep(0.5)

        for track in tracks['forward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(random.random())
        for back_track in tracks['back_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=back_track, yoffset=0).perform()

        # 小范围震荡一下，进一步迷惑极验后台，这一步可以极大地提高成功率
        #ActionChains(self.browser).move_by_offset(xoffset=-3, yoffset=0).perform()
        a = random.uniform(0.1, 0.2)
        time.sleep(round(a, 10))
        ActionChains(self.browser).move_by_offset(xoffset=20, yoffset=0).perform()
        time.sleep(2)
        ActionChains(self.browser).release().perform()
        check = self.success_check()
        if check:
            print('测试成功')
            self.browser.quit()
            return True
        else:
            return False

    def success_check(self):
        """
        验证是否成功
        :return:
        """
        try:
            time.sleep(0.2)
            check = self.browser.find_element_by_xpath('//*[@id="s-authcode"]/div[1]')
            if check.text == '验证成功':

                return True
            else:
                print('验证失败！')
                return False
        except:
            print('加载超时...')


    def  main(self):
        self.get_geetest_image()
        distance = self.get_grap() * (272 / 360) + 19
        tracks = self.get_track(distance)
        slider = c.get_slider()
        if self.move_to_gap(slider, tracks, distance):
            print('验证成功！')
        else:
            print('重新验证')
            return self.main()




if __name__ == '__main__':
    c=CrackGeetest()
    c.main()
