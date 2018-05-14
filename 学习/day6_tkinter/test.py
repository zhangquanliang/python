# -*- coding:utf-8 -*-
"""
author = zhangql
"""
# 第一步
from tkinter import *
from tkinter import messagebox


# 第二步是从Frame派生一个Application类，这是所有Widget的父容器
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hellolaber1 = Label(self, text='hello word')
        self.hellolaber1.pack()
        self.input = Entry()
        self.input.pack()

        # 按钮形式, 点击关闭
        # self.quitbutton = Button(self, text='quit', command=self.quit)
        # self.quitbutton.pack()
        self.hellobutton = Button(self, text='hello', command = self.hello)
        self.hellobutton.pack()

    def hello(self):
        # 用于接受19行输入框的值
        name = self.input.get() or 'word'
        # 弹出提示框
        messagebox.showinfo("提示", 'hello %s' % name)

app = Application()
app.master.title('hello word')

# 进入消息循环
app.mainloop()