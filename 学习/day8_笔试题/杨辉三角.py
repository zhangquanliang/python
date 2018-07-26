# -*- coding:utf-8 -*-
__author__ = '张全亮'


def gen_yanghui(n, yanghui_list = [[1], [1, 1]]):
    if n < 2:
        return yanghui_list[n]
    else:
        for item in range(2, n + 1):
            tmp_list = [1]
            idx = item - 1
            for x in range(len(yanghui_list[idx]) - 1):
                tmp_list.append(yanghui_list[idx][x] + yanghui_list[idx][x+1])
            tmp_list.append(1)
            yanghui_list.append(tmp_list)
        # print "yang:", yanghui_list
    return yanghui_list[n]

print(gen_yanghui(3))