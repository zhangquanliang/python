# -*- coding: utf-8 -*-
import random
list1 = [random.randint(1, 200) for a in range(20)]
list2 = [random.randint(1, 200) for b in range(20)]

print('第一个集合: ', list1)
print('第一个集合: ', list2)
A = set(list1)
B = set(list2)
jiaoji = A.intersection(B)
print('交集: ', jiaoji)
bingji = A.union(B)
print('并集: ', bingji)