# -*- coding=utf-8 -*-
import win32com.client
auto_it = win32com.client.Dispatch('AutoItX3.Control')

# -*- 打开外部程序 -*-
"""
os.system('打开的程序')
ShellExecute("父窗口的句柄，如果没有父窗口，则为0", op , file , params , dir , bShow )
"""


# -*- 键盘控制 -*-
"""
Send("按键"[,参数]) 发送
HotKeySet("热键"[,"自定义功能函数"])  重置热键
"""

# -*- 鼠标控制 -*-
"""
MouseGetCursor() 取鼠标指针类型
MouseGetPos() 取鼠标坐标
MouseDown("按键") 鼠标按下
MouseClickDrag("按键",第一点横坐标,第一点纵坐标,第二点横坐标,第二点纵坐标[,速度]) 鼠标按住拖动
MouseClick("按键"[,横坐标,纵坐标[,次数[,速度]]]) 鼠标点击
MouseUp("按键") 鼠标放开
MouseMove(横坐标,纵坐标[,速度]) 鼠标移动
"""

# -*- 信息框, 对话框 -*-
"""
ProgressOn("标题","主文本"[,"子文本"[,横坐标[,纵坐标[,选项]]]])打开进度条窗口
ProgressOff()关闭进度条窗口
SplashOff() 关闭置顶窗口
ProgressSet(进度值[,"子文本"[,"主文本"]]) 进度设置
InputBox("标题","提示"[,"缺省文本"[,"密码符号"[,宽度,高度[,左边,右边[,等待时间]]]]]) 输入框
MsgBox(按钮参数,"标题","信息文本"[,等待时间]) 信息框
SplashImageOn("标题","图像文件名"[,宽度[,高度[,横坐标[,纵坐标[,选项]]]]]) 置顶图像窗口
SplashTextOn("标题","文本"[,宽度[,高度[,横坐标[,纵坐标[,选项[,"字体名称"[,"字体大小"[,"字体重量"]]]]]]]]) 置顶文本窗口
ToolTip("提示文本"[,横坐标,纵坐标]) 置提示文本
TrayTip("标题","提示文本",等待时间[,图标选项]) 置托盘气泡提示（2000/xp）
"""

# -*- 窗口管理 -*-
"""
WinExists("标题"[,"文字"])窗口是否存在
WinActive("标题"[,"文字"])窗口是否激活
WinSetOnTop("标题","文字",参数)窗口置顶
WinWait("标题"[,"文字"[,等待时间]])等待窗口出现
WinWaitClose("标题"[,"文字"[,等待时间]])等待窗口关闭
WinWaitActive("标题"[,"文字"[,等待时间]])等待窗口激活
WinWaitNotActive("标题"[,"文字"[,等待时间]])等待窗口取消激活状态
WinMenuSelectItem("标题","文字","菜单项1"[,"菜单项2"[,"菜单项3"……]])调用菜单
WinClose("标题"[,"文字"])关闭窗口
WinMinimizeAllUndo()恢复“全部最小化”的窗口
WinActivate("标题"[,"文字"])激活窗口
WinKill("标题"[,"文字"])强制关闭窗口
WinGetTitle("标题"[,"文字"])取窗口标题
WinGetHandle("标题"[,"文字"])取窗口句柄
WinGetClientSize("标题"[,"文字"])取窗口客户区大小
WinGetClassList("标题"[,"文字"])取窗口类列表
WinGetText("标题"[,"文字"])取窗口文字
WinGetCaretPos()取窗口中控件坐标
WinGetState("标题"[,"文字"])取窗口状态
WinGetPos("标题"[,"文字"])取窗口坐标
WinMinimizeAll()全部最小化
WinMove("标题","文字",横坐标,纵坐标[,宽度[,高度]])移动窗口
WinSetTitle("标题","文字","新标题") 置窗口标题
WinSetState("标题","文字",参数) 置窗口状态
"""
