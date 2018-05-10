#coding: utf-8
import threading, time
import socket, struct
from FrameQue import FrameQue

from Logger import logger
from Public import readPackage, opendump, writedump, closedump


##Config###
#########################################################################################################
DUMP_MODE = False
SERVER_LIST = {"face1":{"ip":"zhangql", "port": 2000}}
#SOURCE_LIST = {"face1":{"ip":"192.168.100.167", "port":7001}}
SOURCE_LIST = {"face1":{"ip":"zhangql", "port": 2001}}
# SOURCE_LIST = {"face1":{"ip":"192.168.90.55", "port":20002}}
#########################################################################################################


lock=threading.Lock()
queDic = {}
sourceThreadDic = {}
ServerThreadDic  = {}


def routineSource(name):
    ip = SOURCE_LIST[name]["ip"]
    port = SOURCE_LIST[name]["port"]
    logger.info("source routine " + name + " started, ip=" + ip + " port=" + str(port))

    queue = queDic[name]
    print("ok1")
    while True:
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            
            logger.info("source connecting: " + ip + " " + str(port))
            sock.connect((ip, port))
            logger.info("source connected: " + ip + " " + str(port))

            while True:
                # 接受转发数据
                data = sock.recv(1024)
                print("ok2", data)
                # packdata = readPackage(sock, DUMP_MODE)
                queue.put(data)

        except Exception as e:
            logger.error(str(e))
        finally:
            sock.close()
            time.sleep(3)



def routineDispatch(name, sock_list):
    queue = queDic[name]
    print("ok3")
    while True:
        packdata = queue.get()
        print("ok4")
        for sock in sock_list:
            try:
                sock.sendall(packdata)
            except Exception as e:
                logger.warn(str(e))
                lock.acquire()
                sock_list.remove(sock)
                lock.release()



def routineServer(name):
    ip = SERVER_LIST[name]["ip"]
    port = SERVER_LIST[name]["port"]
    logger.info("server routine " + name + " started, ip=" + ip + " port=" + str(port))

    sock_list = []
    threadDispatch = threading.Thread(target=routineDispatch, args=(name, sock_list))
    threadDispatch.start()

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    while True:  
        _sock,_addr = sock.accept()
        logger.debug(name + ' ==> accept from :' + str(_addr))

        lock.acquire()
        sock_list.append(_sock)
        lock.release()



if __name__ == "__main__":
    logger.info("FACEWARE SCENE SERVER")

    if DUMP_MODE:
        opendump()

    #初始化队列资源
    for name, _ in SOURCE_LIST.items():
        queue = FrameQue()
        queDic[name] = queue

    #启动源线程组
    for name, _ in SOURCE_LIST.items():
        threadSource = threading.Thread(target=routineSource, args=(name,))
        threadSource.start()
        sourceThreadDic[name] = threadSource

    #启动本地服务线程组
    for name, _ in SERVER_LIST.items():
        threadServer = threading.Thread(target=routineServer, args=(name,))
        threadServer.start()
        ServerThreadDic[name] = threadServer


    for name, thread in ServerThreadDic.items():
        thread.join()

