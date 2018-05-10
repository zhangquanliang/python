#coding: utf-8
import threading,time
import socket
from FrameQue import FrameQue

from Logger import logger
from Public import readPackage


#################################################################################
SOURCE_LIST = {"face1":{"ip":"zhangql", "port": 2000}}
# TARGET_LIST = {"face1":{"ip":"192.168.90.55", "port":20001}}
TARGET_LIST = {"face1":{"ip":"zhangql", "port":2001}}
#################################################################################

queDic = {}



def routineTarget(name):
    ip = TARGET_LIST[name]["ip"]
    port = TARGET_LIST[name]["port"]
    logger.info("target routine " + name + " started, ip=" + ip + " port=" + str(port))

    queue = queDic[name]
    print("ok1", queue)
    while True:
        try:
            #连接目标服务器
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            logger.info("target connecting: " + ip + " " + str(port))
            sock.connect((ip, port))
            logger.info("target connected: " + ip + " " + str(port))
            
            while True:
                #从队列取数据发送
                packdata = queue.get()
                # packdata = b'hello'
                sock.sendall(bytes(packdata, encoding='utf8'))
                # print("ok2")
        except Exception as e:
            logger.error("target conn broken: " + str(e))
            sock.close()
        finally:
            time.sleep(3)



def routineSource(name):
    ip = SOURCE_LIST[name]["ip"]
    port = SOURCE_LIST[name]["port"]
    logger.info("source routine " + name + " started, ip=" + ip + " port=" + str(port))

    queue = queDic[name]
    print("ok3")
    while True:
        try:
            #连接源服务器
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            logger.info("source connecting: " + ip + " " + str(port))
            sock.connect((ip, port))
            logger.info("source connected: " + ip + " " + str(port))

            while True:
                #取数据放入队列
                packdata = readPackage(sock)
                queue.put(packdata)
                # print(packdata)
        except Exception as e:
            logger.error("source conn broken: " + str(e))
            sock.close()
            queue.clear()
        finally:
            time.sleep(3)



if __name__ == "__main__":
    logger.info("FACEWARE GATHER SERVER")

    #初始化队列资源
    for name, _ in SOURCE_LIST.items():
        queue = FrameQue()
        queDic[name] = queue


    #启动源线程组
    for name, _ in SOURCE_LIST.items():
        threadSource = threading.Thread(target=routineSource, args=(name,))
        threadSource.start()

    #启动目标线程组
    for name, _ in TARGET_LIST.items():
        threadTarget = threading.Thread(target=routineTarget, args=(name,))
        threadTarget.start()

    


    while True:
        time.sleep(1)

