# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import csv

student_dict = {}
student_id = ""
money = ""
csvFile = open('学生信息.csv', 'w', newline='', encoding='utf8')
writer2 = csv.writer(csvFile)

with open('subsidy_train.csv', 'r', encoding='utf8') as csvfile:
    reader = csv.reader(csvfile)
    for item in reader:
        if item[0] == '学生id':
            student_id = item[0]
            money = item[1]
            continue
        s_id = item[0]
        s_money = item[1].replace('\n', '')
        student_dict[s_id] = s_money

with open('demotest.csv', 'r', encoding='utf8') as csvfile2:
    reader2 = csv.reader(csvfile2)
    for item2 in reader2:
        # xiaofei_dict = {}
        if item2[0] == '学生id':
            writer2.writerow([student_id, "消费时间","其他","图书馆","开水","教务处","文印中心",
                                  "校医院","校车","洗衣房","淋浴","超市","食堂", money])
            continue
        d_id = item2[0]
        if d_id in student_dict.keys():
            d_money = student_dict[d_id]
        else:
            d_money = '0'
        d_xfrq = item2[1].replace('\n', '')
        d_qt = item2[2].replace('\n', '')
        d_tsg = item2[3].replace('\n', '')
        d_ks = item2[4].replace('\n', '')
        d_jwc = item2[5].replace('\n', '')
        d_wyzx = item2[6].replace('\n', '')
        d_xyy = item2[7].replace('\n', '')
        d_xc = item2[8].replace('\n', '')
        d_xyf = item2[9].replace('\n', '')
        d_ly = item2[10].replace('\n', '')
        d_cs = item2[11].replace('\n', '')
        d_st = item2[12].replace('\n', '')
        writer2.writerow([d_id, d_xfrq, d_qt, d_tsg, d_ks, d_jwc, d_wyzx,
                          d_xyy, d_xc, d_xyf, d_ly, d_cs, d_st, d_money])
        # xiaofei_dict["d_id"] = d_id
        # xiaofei_dict["d_xfrq"] = d_xfrq
        # xiaofei_dict["d_qt"] = d_qt
        # xiaofei_dict["d_tsg"] = d_tsg
        # xiaofei_dict["d_ks"] = d_ks
        # xiaofei_dict["d_jwc"] = d_jwc
        # xiaofei_dict["d_wyzx"] = d_wyzx
        # xiaofei_dict["d_xyy"] = d_xyy
        # xiaofei_dict["d_xc"] = d_xc
        # xiaofei_dict["d_xyf"] = d_xyf
        # xiaofei_dict["d_ly"] = d_ly
        # xiaofei_dict["d_cs"] = d_cs
        # xiaofei_dict["d_st"] = d_st


csvFile.close()
