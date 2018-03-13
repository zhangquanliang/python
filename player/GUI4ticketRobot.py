#coding=utf-8
import smtplib
import poplib
import os
import json
import tkinter
from  tkinter import messagebox
import time
import requests
from multiprocessing.dummy import Pool

from merchandise import buy_player, sale_palyer, get_html
# from shoppingRobot import login


class Window():
    """
    窗体类，进行窗体的布局，函数的调用
    里面的所有操作必须使用多线程，不然窗口会假死
    """
    def __init__(self,root):
        global good_list, author_info
        self.tag = True
        self.buy_status = False
        self.sale_status = False
        good_list = []
        self.author_info = {"session": '', 'sid': '', 'token': ''}
        self.pool = Pool()

        self.label1 = tkinter.Label(root, text='账号')
        self.label2 = tkinter.Label(root, text='密码')
        self.label3 = tkinter.Label(root, text='UT答案')
        self.label4 = tkinter.Label(root, text='球员品质')
        self.label5 = tkinter.Label(root, text='球员姓名')
        self.label6 = tkinter.Label(root, text='购买最高价')
        self.label7 = tkinter.Label(root, text='出售最高价')
        self.label8 = tkinter.Label(root, text='购买最低价')
        self.label9 = tkinter.Label(root, text='出售最低价')

        # 备用接口标签，用于接收购买的url参数
        self.label10 = tkinter.Label(root, text='Session')
        self.label11 = tkinter.Label(root, text='Sid')
        self.label12 = tkinter.Label(root, text='Token')

        # 日志框提示信息标签
        self.label13 = tkinter.Label(root, text='\n█\n█\n█\n█\n█\n█\n日\n志\n框\n在\n此\n█\n█\n█\n█\n█\n█')

        self.label14 = tkinter.Label(root, text='线程数量')
        self.label15 = tkinter.Label(root, text='自动购买工作状态>>>')
        # self.label16 = tkinter.Label(root, text='工作状态')

        self.label1.place(x=5, y=5)
        self.label2.place(x=5, y=30)
        self.label3.place(x=5, y=55)
        self.label4.place(x=5, y=80)
        self.label5.place(x=5, y=105)
        self.label6.place(x=5, y=130)
        self.label7.place(x=5, y=155)
        self.label8.place(x=220, y=130)
        self.label9.place(x=220, y=155)

        # 备用接口标签位置
        self.label10.place(x=220, y=5)
        self.label11.place(x=220, y=30)
        self.label12.place(x=220, y=55)

        self.label13.place(x=20, y=210)  # 日志提示框的位置
        self.label14.place(x=220, y=80)  # 线程数量标签的位置
        self.label15.place(x=500, y=5)

        self.entry_sm = tkinter.Entry(root)
        self.entry_po = tkinter.Entry(root, show='*')
        self.entry_user = tkinter.Entry(root)
        self.entry_pw = tkinter.Entry(root)
        self.entry_rece = tkinter.Entry(root)
        self.entry_topic = tkinter.Entry(root)
        self.sender = tkinter.Entry(root)
        self.sall_price = tkinter.Entry(root)
        self.buy_min_price = tkinter.Entry(root)
        self.thread_nums = tkinter.Entry(root)      # 线程数量输入框

        # 备用接口输入框，接收自动购买的url参数
        self.session = tkinter.Entry(root)
        self.sid = tkinter.Entry(root)
        self.token = tkinter.Entry(root)

        self.entry_sm.place(x=70, y=5)
        self.entry_po.place(x=70, y=30)
        self.entry_user.place(x=70, y=55)
        self.entry_pw.place(x=70, y=80)
        self.entry_rece.place(x=70, y=105)
        self.entry_topic.place(x=70, y=130)
        self.buy_min_price.place(x=290, y=130)
        self.sender.place(x=70,y=155)
        self.sall_price.place(x=290, y=155)
        self.thread_nums.place(x=290, y=80)

        # 备用接口输入框的位置布局
        self.session.place(x=290, y=5)
        self.sid.place(x=290, y=30)
        self.token.place(x=290, y=55)

        # 信息以前日志输出框
        self.text = tkinter.Text(root)
        self.text.place(y=220, x=50, width=680, height=350)
        # 为日志输入框添加纯质滚动条
        self.vscroll = tkinter.Scrollbar(self.text)
        self.vscroll.pack(side='right', fill='y')
        self.text['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.text.yview

        # 工作状态的text输入框
        self.text_runing_status = tkinter.Text(root)
        self.text_runing_status.place(y=25, x=500, width=250, height=50)

        self.button = tkinter.Button(root,text='开始购买',command=self.buy)
        self.button.place(x=50,y=184)
        self.button_stop_buy = tkinter.Button(root, text='暂停购买', command=self.stop_buy)
        self.button_stop_buy.place(x=120, y=184)
        self.btn_aotu_sale = tkinter.Button(root, text='开启出售', command=self.sale)
        self.btn_aotu_sale.place(x=190,y=184)
        self.btn_stop_aotu_sale = tkinter.Button(root, text='关闭出售', command=self.stop_sale)
        self.btn_stop_aotu_sale.place(x=260, y=184)
        self.btn_clear_logbox = tkinter.Button(root, text='清空日志框', command=self.clear_logbox)
        self.btn_clear_logbox.place(x=330, y=184)

        self.root = root

    def buy(self):
        if self.buy_status:
            return
        info_dict = self.get_info()
        def to_buy():
            session = info_dict['session']
            sid = info_dict['sid']
            token = info_dict['token']
            player_name = info_dict['player_name']
            max_price = info_dict['buy_max']
            min_price = info_dict['buy_min']
            quality = info_dict['quality']
            self.buy_status = True
            while self.buy_status:
                result = buy_player(session, sid, token, min_price, max_price, player_name, quality=quality)
                success = result['success']
                if success:
                    buy_now_price = result['price']
                    buy_time = result['time']
                    # 如果购买成功将日志输出到日志栏
                    self.text.insert(tkinter.END, '[{} 购买成功] [购买价格:{}] [时间:{}] [价格区间:({})---({})]\n'.format(
                        player_name, buy_now_price, buy_time, min_price, max_price))
                if success == False and result['code'] in (500, 401) :
                    self.send_buy_status(1000, error=result['error'])
                    self.text.insert(tkinter.END, '参数已失效，请重新获取！！！\n')
                else:
                    # self.send_buy_status(1000,error=result['error'])
                    pass
                time.sleep(0.2)        # 测试使用

        thread_nums = int(info_dict['thread_nums'])
        for i in range(thread_nums):
            self.pool.apply_async(to_buy)  # 购买函数所需的函数  session,sid,token,min_price,max_price
        self.text.insert(tkinter.END, '自动购买已开启\n\n')
        self.send_buy_status(True, thread_nums)

    def sale(self):
        if self.sale_status:
            return
        def to_sale():
            info_dict = self.get_info()
            session = info_dict['session']
            sid = info_dict['sid']
            token = info_dict['token']
            player_name = info_dict['player_name']
            max_price = info_dict['sale_max']
            min_price = info_dict['sale_min']
            player_id = ""
            hold_time = ""
            self.sale_status = True
            while self.sale_status:
                mess = True
                # mess = buy_player(session, sid, token, min_price, max_price)
                if mess:
                    # 如果出售成功将日志输出到日志栏
                    self.text.insert(tkinter.END, '{} 出售成功 价格区间:({})---({})\n'.format(player_name, min_price, max_price))
                # self.text.insert(tkinter.END, '出售成功') # 测试使用
                time.sleep(0.5)                           # 测试使用
        for i in range(2):
            self.pool.apply_async(to_sale)  # 出售函数参数 session,sid,token,min_price,max_price,player_id,hold_time
        pass

    def stop_buy(self):
        self.buy_status = False
        self.text.insert(tkinter.END, '自动购买已关闭\n\n')
        self.send_buy_status(self.buy_status)
        pass

    def stop_sale(self):
        self.sale_status = False
        self.text.insert(tkinter.END, '自动出售已关闭\n\n')
        pass

    def login(self):
        pass

    def send_buy_status(self, status, thread_nums=2, **kwargs):
        self.text_runing_status.delete(0.0, tkinter.END)
        if status == True:
            self.text_runing_status.insert(tkinter.END, '自动购买：自动购买正在运行,请等待\n'
                                                        '当前线程数量：{}\n线程状态:正常'.format(thread_nums))
        elif status == False:
            self.text_runing_status.insert(tkinter.END, '自动购买已关闭')
        if status != 200:
            self.buy_status = False
            self.text_runing_status.insert(tkinter.END, '程序已停止\n原因：{}\n'.format(kwargs['error']))
            self.text.delete(0.0, tkinter.END)
            self.text.insert(tkinter.END, '程序已停止\n原因：{}\n'.format(kwargs['error']))

    def get_info(self):
        # 从输入框获取参数信息
        info_dict = {}
        info_dict['account'] = self.entry_sm.get().strip()
        info_dict['password'] = self.entry_po.get().strip()
        info_dict['ut_answer'] = self.entry_user.get().strip()
        info_dict['quality'] = self.entry_pw.get().strip()
        info_dict['player_name'] = self.entry_rece.get().strip()
        info_dict['buy_max'] = self.entry_topic.get().strip()
        info_dict['buy_min'] = self.buy_min_price.get().strip()
        info_dict['sale_max'] = self.sender.get().strip()
        info_dict['sale_min'] = self.sall_price.get().strip()
        info_dict['session'] = self.session.get().strip()
        info_dict['sid'] = self.sid.get().strip()
        info_dict['token'] = self.token.get().strip()
        info_dict['thread_nums'] = self.thread_nums.get().strip()

        if info_dict['thread_nums'] == '':
            info_dict['thread_nums'] = 2
        if int(info_dict['thread_nums']) > 4:
            info_dict['thread_nums'] = 4

        path = 'params.json'
        with open(path, 'w') as f:
            f.write(json.dumps(info_dict))
        return info_dict

    def load_params(self):
        path = 'params.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                info_dict = json.loads(f.read())
                self.entry_sm.insert('end', info_dict['account'])
                self.entry_po.insert('end', info_dict['password'])
                self.entry_user.insert('end', info_dict['ut_answer'])
                self.entry_pw.insert('end', info_dict['quality'])
                self.entry_rece.insert('end', info_dict['player_name'])
                self.entry_topic.insert('end', info_dict['buy_max'])
                self.buy_min_price.insert('end', info_dict['buy_min'])
                self.sender.insert('end', info_dict['sale_max'])
                self.sall_price.insert('end', info_dict['sale_min'])
                self.session.insert('end', info_dict['session'])
                self.sid.insert('end', info_dict['sid'])
                self.token.insert('end', info_dict['token'])
                self.thread_nums.insert('end', info_dict['thread_nums'])

    def clear_logbox(self):
        yes_or_no = tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
        if yes_or_no:
            self.text.delete(0.0, tkinter.END)

    def close_window(self):
        answer = tkinter.messagebox.askyesno('退出', '是否退出程序')
        if answer:
            self.root.destroy()


def show():
    root = tkinter.Tk()
    root.title("球员自动买入卖出程序")
    root.geometry('800x600+800+300')
    window = Window(root)
    window.load_params()
    root.minsize(380,450)
    root.protocol('WM_DELETE_WINDOW', window.close_window)      # 防止意外关闭
    root.mainloop()


if __name__ == '__main__':
    show()