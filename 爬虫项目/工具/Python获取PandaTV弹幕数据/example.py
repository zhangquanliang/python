# 将用户昵称及其发言内容存入excel
from openpyxl import Workbook
from Get_PD_Barrage import Get_Barrage


if __name__ == '__main__':
	wb = Workbook()
	ws = wb.active
	room_id = input('请输入PandaTV房间号：')
	danmu = Get_Barrage(room_id)
	danmu_data = danmu.get_buffer()
	count = 0
	while True:
		# 采集到的弹幕数量大于100时停止采集
		if count > 100:
			danmu.stop()
			break
		if len(danmu_data) > 0:
			data = danmu_data.pop(0)
			try:
				ws.append([data['data']['from']['nickName'], data['data']['content']])
				count += 1
				print('第%d条弹幕保存成功！' % count)
			except:
				pass
	wb.save('./results/' + room_id + '.xlsx')