import requests
import websocket
import math
import time
import json
from threading import Thread


class Get_Barrage():
	def __init__(self, room_id):
		self.__room_id = room_id
		self.__url = 'https://riven.panda.tv/chatroom/getinfo'
		self.__data = {
			'roomid': self.__room_id,
			'app': 1,
			'protocol': 'ws',
			'_caller': 'panda-pc_web',
			'_': math.floor(time.time())
			}
		self.__headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
			}
		self.__res_data = None
		self.__ws = None
		self.__done = True
		self.__buffer = []
		Thread(target=self.connect_to_Panda, name='Connect-PandaTV-Barrage').start()
	# 获取采集到的数据
	def get_buffer(self):
		return self.__buffer
	# 停止采集
	def stop(self):
		self.__done = False
		self.__ws.close()
	# 建立和弹幕服务器的连接
	def connect_to_Panda(self):
		self.res = requests.get(self.__url, self.__data, headers=self.__headers, verify=False)
		self.res_json = json.loads(self.res.text)
		self.__res_data = self.res_json['data']
		self.ws_url = self.res_json['data']['chat_addr_list'][0]
		websocket.enableTrace(True)
		self.ws = websocket.WebSocketApp('wss://' + self.ws_url)
		self.ws.on_open = self.on_open_ws
		self.ws.on_message = self.on_message_ws
		self.__ws = self.ws
		self.ws.run_forever(origin='https://www.panda.tv')
	# 通过心跳包维持和弹幕服务器的WebSocket连接
	def on_open_ws(self, ws):
		self.msg = 'u:{}@{}\n' \
				   'ts:{}\n' \
				   'sign:{}\n' \
				   'authtype:{}\n' \
				   'plat:jssdk_pc_web\n' \
				   'version:0.5.9\n' \
				   'pdft:\n' \
				   'network:unknown\n' \
				   'compress:zlib'.format(self.__res_data['rid'], self.__res_data['appid'], self.__res_data['ts'],
				   						  self.__res_data['sign'], self.__res_data['authType'])
		self.header = bytes.fromhex('00060002') + len(self.msg).to_bytes(2, byteorder='big')
		self.content = bytes(self.msg, encoding='utf-8')
		self.__ws.send(self.header+self.content, opcode=websocket.ABNF.OPCODE_BINARY)
		# 发心跳包
		self.heartbeats_package = Thread(target=self.send_HB_package, name='Send-HeartBeats-Package')
		self.heartbeats_package.start()
	# 每隔一段时间向弹幕服务器发送心跳包
	def send_HB_package(self):
		while self.__done:
			time.sleep(30)
			self.heartbeat_package = bytes.fromhex('00060000')
			self.__ws.send(self.heartbeat_package, opcode=websocket.ABNF.OPCODE_BINARY)
	# 处理弹幕服务器传来的数据
	def on_message_ws(self, ws, message):
		if len(message) < 5:
			return
		self.op = int.from_bytes(message[2:4], byteorder='big')
		if self.op == 3:
			self.barrages_str = message.decode('utf-8', 'ignore')
			try:
				self.normal_barrage = "\"type\":\"1\""
				if self.normal_barrage in self.barrages_str:
					self.p1 = self.barrages_str.find('{' + self.normal_barrage)
					self.p2 = self.barrages_str.rfind('{' + self.normal_barrage)
					if self.p1 == self.p2:
						self.__buffer.append(json.loads(self.barrages_str[self.p1:]))
					else:
						self.p1_end = self.barrages_str[self.p1:self.p2].rfind('}') + 1
						self.barrage1 = json.loads(self.barrages_str[self.p1:self.p1_end])
						self.barrage2 = json.loads(self.barrages_str[self.p2:])
						self.__buffer.append(self.barrage1)
						self.__buffer.append(self.barrage1)
			except json.JSONDecodeError:
				pass



if __name__ == '__main__':
	room_id = input('请输入PandaTV房间号：')
	danmu = Get_Barrage(room_id).get_buffer()
	print(danmu)
	while True:
		try:
			if len(danmu) > 0:
				danmu_data = danmu.pop(0)
				print('用户：%s\n内容：%s' % (danmu_data['data']['from']['nickName'], danmu_data['data']['content']))
		except KeyboardInterrupt:
			danmu.stop()
			break