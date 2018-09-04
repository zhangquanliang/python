# 作为模块导入的使用示例
from .Get_PD_Barrage import Get_Barrage

# 初始化
room_id = 1922546
danmu = Get_Barrage(room_id)
# 获取弹幕数据
danmu.get_buffer()
# 终止连接(即停止弹幕采集)
danmu.stop()

# 使用举例
room_id = 1922546
danmu = Get_Barrage(room_id).get_buffer()
while True:
	try:
		if len(danmu) > 0:
			danmu_data = danmu.pop(0)
			print('用户：%s\n内容：%s' % (danmu_data['data']['from']['nickName'], danmu_data['data']['content']))
	except KeyboardInterrupt:
		danmu.stop()
		break