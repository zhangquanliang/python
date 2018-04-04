# -*- coding: utf-8 -*-
"""简化了方法名"""

# class Num:
#     def __init__(self):
#         self.__num = 100
#
#     def setNum(self, num):
#         print('------setNum------')
#         self.__num = num
#
#     def getNum(self):
#         print('------getNum------')
#         return self.__num
#
#     num_ = property(getNum, setNum)
#
# num = Num()
# num.num_ = 102121
# print(num.num_)

class Money:
    def __init__(self):
        self.moneys = 12

    @property
    def money(self):
        return self._moneys

    @money.setter
    def money(self, value):
        self._moneys = value


mo = Money()
mo.money = 200
print(mo.money)