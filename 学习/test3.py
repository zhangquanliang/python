from tkinter import *
from tkinter import ttk

bookList = [('aaa', 123), ('bbb', 123), ('xxx', 123), ('sss', 123), ('ddd', 123)]
root = Tk()
frame = ttk.Frame(root)
frame.pack(fill='both', expand='false')
tree = ttk.Treeview(frame, columns=['name', 'price'], show='headings')
tree.heading('name', text='name')
tree.heading('price', text='price')
for item in bookList:
    tree.insert('', 'end', values=item)
tree.pack()

root.mainloop()

