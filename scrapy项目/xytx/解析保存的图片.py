# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import os
import sys
import xlwt
from aip import AipOcr

APP_ID = '11294671'
API_KEY = 't8SdmqrHnCe9zgIv4bzB6CKc'
SECRET_KEY = 'qEc9mhG7IFZLXkwnhbeN8Tfl2wdObmYn'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
sheet = book.add_sheet("Sheet")     # 添加Excel页签
sheet.write_merge(0, 0, 0, 3, '信游天下')
sheet.write(1, 0, '电话')
sheet.write(1, 1, '地址')
i = 2


# 解析图片
def parse_image():
    rootdir = sys.path[0] + '\images'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            image = get_file_content(path)
            """ 调用通用文字识别, 图片为本地图片 """
            result = client.general(image)
            parse_dict(result)
        # break

    excel_path = r'信游天下' + '.xls'
    book.save(excel_path)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def parse_dict(result):
    t = []
    global i
    for t_dict in result['words_result']:
        if '地址' in str(t_dict['words']):
            dizhi = t_dict['words']
            t.append(dizhi)
        if '电话' in str(t_dict['words']) or '热线' in str(t_dict['words']):
            dianhua = t_dict['words']
            t.append(dianhua)
    if len(t) == 0 or len(t) == 1:
        return
    if '地址' in t[0]:
        t = list(reversed(t))
    sheet.write(i, 0, t[0])
    sheet.write(i, 1, t[1:])
    print(t)
    i += 1


if __name__ == '__main__':
    parse_image()