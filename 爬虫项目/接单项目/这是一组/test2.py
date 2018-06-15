# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import re
import xlwt
from collections import defaultdict
book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
sheet = book.add_sheet("Sheet")     # 添加Excel页签
# w_zhang = 2
w_lines = 1

with open('14.txt', 'r', encoding='utf8') as f:
    f_data = f.readlines()
mapping_child_chapter = ['―', '一', '二', '三', '四', '五', '六', '七', '八', '九', '囬']


def get_next_layer(line, type_t):
    if type_t == 1:
        title = re.search('第(.)章', line)
        if title:
            return (True, title.group(1))
        else:
            return (False, None)
    if type_t == 2:
        match_str = [i + '、' for i in mapping_child_chapter]
        for j in match_str:
            title = re.search(j, line)
            if title:
                return (True, title.group(0))
        return (False, None)
    if type_t == 3:
        match_str = ['\({}\）'.format(i) for i in mapping_child_chapter]
        for j in match_str:
            title = re.search(j, line)
            if title:
                return (True, title.group(0))
        return (False, None)

    if type_t == 4:
        match_str = ['\d+\.'.format(i) for i in mapping_child_chapter]
        for j in match_str:
            title = re.search(j, line)
            if title:
                return (True, title.group(0))
        return (False, None)


def parse_txt():
    # global w_zhang
    global w_lines
    chapter_container = defaultdict(list)
    chapter = ''
    for i in f_data:
        ret = get_next_layer(i, 1)
        if ret[0]:
            chapter = ret[1]
        chapter_container[chapter].append(i)
    chapter_container_keys = chapter_container.keys()

    # 循环章节
    for c_key in chapter_container_keys:
        wb_zhang = str(chapter_container[c_key][:1][0]).replace('\n', '')
        sheet.write(w_lines, 0, wb_zhang)
        title_container = defaultdict(list)
        title = ''
        w_lines += 3
        # 每个章节
        for j in chapter_container[c_key]:
            ret = get_next_layer(j, 2)
            if ret[0]:
                title = ret[1].replace('、', '')
            j = j.replace('[', '').replace(']', '').replace('\t', '').replace('\t', '').replace('、', '').replace('\n', '').replace("'", '')
            title_container[title].append(j)

        title_container_keys = title_container.keys()
        for t_key in title_container_keys:
            wb_title = str(title_container[t_key][:1][0]).replace('\n', '')
            sheet.write(w_lines, 0, wb_title)
            type_container = defaultdict(list)
            type_t = ''
            w_lines += 1
            # 取title为一的症状
            for h in title_container[t_key]:
                ret = get_next_layer(h, 3)
                if ret[0]:
                    type_t = ret[1].replace('(', '').replace('）', '')
                h = h.replace('[', '').replace(']', '').replace('\t', '').replace('\t', '').replace('、', '').replace('\n', '').replace("'", '')
                type_container[type_t].append(h)
            type_container_keys = title_container.keys()
            for type_key in type_container_keys:
                if len(type_container[t_key]) == 0:
                    continue
                tp_title = str(type_container[t_key][:1][0]).replace('\n', '')
                sheet.write(w_lines, 0, tp_title)
                line_container = defaultdict(list)
                line = ''
                # 取类型为一的类型
                for e in type_container[type_key]:
                    ret = get_next_layer(e, 4)
                    if ret[0]:
                        line = ret[1].replace('.', '')
                    e = e.replace('[', '').replace(']', '').replace('\t', '').replace('\t', '').replace('、', '').replace('\n', '').replace("'", '')
                    line_container[line].append(e)

                line_container_keys = line_container.keys()
                for line_ley in line_container_keys:
                    # 取类型中以1开始的文件
                    s = str(line_container[line_ley]).replace('\n', '').replace("'", '')
                    print(c_key, chapter_container[c_key][:1][0], title_container[t_key][:1][0])
                w_lines += 1
            w_lines += 1
        # w_zhang += w_lines+2
        w_lines += 3

if __name__ == '__main__':
    parse_txt()
    path = r'文件111.xls'
    book.save(path)
