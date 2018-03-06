# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image, ImageEnhance

im=Image.open(r"D:\Git\MyProject\project\test\1.png")
imgry = im.convert('L')#图像加强，二值化
sharpness =ImageEnhance.Contrast(imgry)#对比度增强
sharp_img = sharpness.enhance(2.0)
sharp_img.save(r"D:\Git\MyProject\project\test\2.png")
ima = r'D:\Git\MyProject\project\test\2.png'
code = pytesseract.image_to_string(ima)
print(code)