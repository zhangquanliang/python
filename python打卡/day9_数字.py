# -*- coding: utf-8 -*-


# 1. 内嵌整数列表中的指相加
def nested_sum(t):
    a = 0
    for x in t:
        for y in x:
            a += y
    print(a)


# 2. 接受数字列表，返回累计和
def cumsum(t):
    list = []
    a = 0
    for x in t:
        a += x
        list.append(a)
    print(list)


# 3. 接受一个列表，返回新列表，包含除第一个和最后一个元素外的所有值
def middle(t):
    t.pop(0)
    t.pop()
    print(t)

# t = [1, 2, 3, 4, 1212, 121]
# middle(t)


# 4. 斐波纳契数列
a, b = 0, 1
for i in range(1, 13):
    print('第%s个月：%s对兔子' % (i, b))
    a, b = b, a + b