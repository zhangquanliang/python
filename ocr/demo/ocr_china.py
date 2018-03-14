# -*- coding: utf-8 -*-
"""
文字识别
"""
import pytesseract
from aip import AipOcr
from PIL import Image, ImageEnhance


class Ocr:
    def __init__(self):
        config = {
            'appId': '10914896',
            'apiKey': 'R5LAXesAqaNYunPWLb5UHM3h',
            'secretKey': 'RdLi2pn2usBfGVTSSHedQUlrkO1FUnIV'
        }
        self.client = AipOcr(**config)

    # 使用百度提供的OCR文字识别
    def ocr_aip_china(self, image_path):
        file = open(image_path, 'rb')
        image = file.read()
        file.close()
        result_ = self.client.basicGeneral(image)
        if "words_result" in result_:
            result = "\n".join([w['words'] for w in result_['words_result']])
            return result

    # 通过python模块pytesseract识别文字
    def ocr_tesseract_china(self, image_path):
        tessdata_dir_config = r'--tessdata-dir "D:\Git\MyProject\zhangql\ocr\Tesseract-OCR\tessdata"'
        image = Image.open(image_path)
        enhance = ImageEnhance.Contrast(image)
        image_enhance = enhance.enhance(4)
        text = pytesseract.image_to_string(image_enhance, config=tessdata_dir_config, lang='chi_sim')
        # text = pytesseract.image_to_string(image, model_zql=tessdata_dir_config, lang='chi_sim')
        return text


if __name__ == '__main__':
    ocr = Ocr()
    # china = ocr.ocr_aip_china(r'D:\Git\MyProject\zhangql\ocr\demo\test7.png')
    china = ocr.ocr_tesseract_china(r'D:\Git\MyProject\zhangql\ocr\demo\test10.png')
    print(china)