'''
菜单栏操作   WinMenuSelectItem(“窗口标题”,"", ”主菜单” , ”子菜单1”, ”子菜单2” „„)  点击子菜单
工具栏操作   ControlCommand(“窗口标题”, "窗口文本", ”工具栏控件名” , "SendCommandID", ”控件ID”)  点击工具栏
表单控件操作 1、文本框  ControlSetText(“标题”,"",”控件名或ID” ,”输入的字符串数据”) 输入数据
                       ControlGetText(“标题”,"",”控件名或ID”) 获取文本框数据
            2、选择控件 ControlCommand(“窗口标题”, "", 控件类名或ID , "SelectString", 选中选项文本) 如选择下拉框的某个选项：
                       ControlCommand(“窗口标题”, "",控件类名或ID ,"check", ””)
点击操作    1、控件点击 ControlClick("窗口标题","","控件名或ID","按钮","点击次数") 按钮分左键(left)，右键(right)等
            2、鼠标点击 MouseClick(“按钮”, “X坐标”,”Y坐标”,”点击次数”)
窗口操作    1、激活指定窗口 WinActivate("窗口标题", "")
            2、最大化窗口 WinSetState("窗口标题", "", @SW_MAXIMIZE)
键盘操作    1、一般字符  Send("向光标激活地方发送的字符串") 向当前激活窗口文本框，发送按键字符
            2、快捷字符 Send("^s")保存  Send(“{ PRINTSCREEN}”)截屏键  Send(“{ SPACE}”)空格键  Send(“{ ENTER}”)回车键
像素操作    1、WinGetPos("窗口标题","") 得到系统窗口位置
            2、ControlGetPosX  得到控件位置坐标
文件操作    1、一般文件 FileOpen("文件", 0)打开文件    FileCopy("原文件", "目标文件或路径", 1) 复制文件
            2、ini文件 iniRead ( "文件名", "字段名", "关键字", "默认值")读取文件 iniWrite ( "文件名", "字段名", "键名", "值") 写入ini文件
windows锁屏处理  1、Send 命令必须要在激活窗口的条件下才能正确执行
                2、ControlSend命令可以不需要激活窗口就能执行

WinExists    检验窗口是否存在
win32api.ShellExecute    使用ShellExecute函数运行其他程序ShellExecute(hwnd, op , file , params , dir , bShow )
WinWait   目标窗口标题
WinGetClassList   获取指定窗口的所有控件类的列表.WinGetClassList ( "窗口标题" [, "窗口文本"] )
WinActive  激活指定窗口，使其成功活动状态  WinActivate(class_main_form)
ControlGetText 从一个窗口获取文本
ControlFocus 在一个窗口的特定控件上设置焦点 auto_it.ControlFocus(self.class_login, "", control_id)
ControlClick 在一个窗口的特定控件上点击 ControlClick(class_login, "", "TFBPanel4")、
ControlSetText 从一个窗口设置文本
WinWaitClose  暂停脚本的执行，直到请求的窗口不存在为止
WinSetOnTop   更改窗口的“始终在顶部”属性。auto_it.WinSetOnTop(self.class_main_form, "", 1)  # 设置窗口状态：置顶
WinGetPosX 得到系统窗口位置
ControlGetPosX  得到控件位置坐标
print auto_it.ControlGetPosX('[CLASS:CabinetWClass]', '', 'DirectUIHWND1')
'''
