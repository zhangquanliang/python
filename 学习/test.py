# -*- coding: utf-8 -*-
from captcha.image import ImageCaptcha
from PIL import Image
import numpy  as np
class YZM:
    def __init__(self):
        pass

    def save_yzm1(self):
        text = 'awda'
        image = ImageCaptcha()
        captcha = image.generate(text)
        captcha_image = Image.open(captcha)
        captcha_image.save('1.png')
        captcha_image.show()
    def save_yzm2(self, captcha_text):
        VOCAB = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        CAPTCHA_LENGTH = 4
        VOCAB_LENGTH = len(VOCAB)
        image = ImageCaptcha()
        captcha = image.generate(captcha_text)
        captcha_image = Image.open(captcha)
        captcha_array = np.array(captcha_image)
        return captcha_array

    def sb_yzm(self):
        pass

if __name__ == '__main__':
    sc_yzm = YZM()
    captcha = sc_yzm.save_yzm2('1234')
    print(captcha, captcha.shape)
    # sb_yzm = YZM()
    # sb_yzm.sb_yzm()