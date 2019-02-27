import tkinter
from tkinter import ttk  # 导入内部包
from 移动门户爬虫 import get_data

win = tkinter.Tk()
tree = ttk.Treeview(win)  # 表格
tree["columns"] = (
"OPER_ID", "ORG_ID", "PHONE", "PHONE_NO", "PHONE_TEXT", "P_PRODUCT_NAME", "phone_traffic", "phone_Consumption",
"phone_call")
tree.column("OPER_ID", width=100)  # 表示列,不显示
tree.column("ORG_ID", width=100)
tree.column("PHONE", width=100)
tree.column("PHONE_NO", width=100)
tree.column("PHONE_TEXT", width=100)
tree.column("P_PRODUCT_NAME", width=100)
tree.column("phone_traffic", width=100)
tree.column("phone_Consumption", width=100)
tree.column("phone_call", width=100)

tree.heading("OPER_ID", text="开放ID")  # 显示表头
tree.heading("ORG_ID", text="组织标识")
tree.heading("PHONE", text="电话")
tree.heading("PHONE_NO", text="电话编号")
tree.heading("PHONE_TEXT", text="客户画像")
tree.heading("P_PRODUCT_NAME", text="推荐套餐")
tree.heading("phone_traffic", text="流量")
tree.heading("phone_Consumption", text="消费")
tree.heading("phone_call", text="通话")
[OPER_ID, ORG_ID, PHONE, PHONE_NO, phone_text, P_PRODUCT_NAME, phone_traffic, phone_Consumption, phone_call] = get_data(
    '20178222', '40122056', '123',
    '-119,-115,50,22,-23,-49,-3,-43,125,-115,27,31,30,70,-37,74,94,32,-51,-116,115,100,-52,-122,-2,-61,-33,2,112,-36,-103,35,-45,4,65,57,-83,-62,-79,83,47,-44,27,121,-31,-28,-78,47,113,-112,-106,2,89,99,-77,51,-17,117,-104,59,40,102,30,44,111,69,19,12,-18,-77,68,-68,-34,-106,-120,-70,-65,-5,-93,-35,0,97,94,73,101,-84,-105,21,8,87,-6,-113,-100,-6,27,-33,112,46,9,13,-86,53,-46,-69,-66,-30,55,-121,-19,72,-22,78,55,98,-1,33,45,-41,-119,-80,-128,63,-40,45,30,-106,-22,0')

print(OPER_ID, ORG_ID, PHONE, PHONE_NO, phone_text, P_PRODUCT_NAME, phone_traffic, phone_Consumption, phone_call)

tree.insert("", 0, text="Success", values=(
OPER_ID, ORG_ID, PHONE, PHONE_NO, phone_text, P_PRODUCT_NAME, phone_traffic, phone_Consumption, phone_call))  # 插入数据，
tree.insert("", 1, text="line1", values=("1", "2", "3"))
tree.insert("", 2, text="line1", values=("1", "2", "3"))
tree.insert("", 3, text="line1", values=("1", "2", "3"))
tree.insert("", 4, text="line1", values=("1", "2", "3"))
tree.insert("", 5, text="line1", values=("1", "2", "3"))
tree.insert("", 6, text="line1", values=("1", "2", "3"))
tree.insert("", 7, text="line1", values=("1", "2", "3"))

tree.pack()
win.mainloop()
