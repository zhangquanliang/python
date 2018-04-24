# -*- coding: utf-8 -*-


def demo(L):
    k = len(L)
    if k >= 10:
        if L.isalnum() and not L.isdigit() and not L.isalpha()and not L.isspace():
            return print("是强密码")
        else:
            L = L.replace("!","")
            L = L.replace("_","")
            L = L.replace("#","")
            L = L.replace("@","")
            m = len(L)

            if k != m and L.isalnum()and not L.isdigit() and not L.isalpha():
                return print("是强密码")
            elif k != m and L.isalpha() and not L.lower() in L and not L.upper() in L:
                return print("是强密码")
            else:
                return print("不是强密码")
    else:
        return print("不是强密码")


L = input("请输入一组密码:")
demo(L)