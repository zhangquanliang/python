#coding: utf-8
import threading,time
import socket,struct
from FrameQue import FrameQue
from Logger import logger
from Public import readPackage


##Config###
#########################################################################################################
LOCAL_HOST = "zhangql"
# LOCAL_HOST = "172.17.50.248"
INPUT_PORTS  = {"face1":2000}
OUTPUT_PORTS = {"face1":2001}
#########################################################################################################


lock=threading.Lock()
queDic = {}
global_data = []


def routineDispatch(name, sock_list):
    queue = queDic[name]
    
    while True:
        #取数据
        packdata = queue.get()

        try:
            for sock in sock_list:
                sock.sendall(packdata)
        except Exception as e:
            logger.error(str(e))
            lock.acquire()
            sock_list.remove(sock)
            lock.release()



def routineInPut(name):
    ip = LOCAL_HOST
    port = INPUT_PORTS[name]
    logger.info("input routine " + name + " started, ip=" + ip + " port=" + str(port))

    queue = queDic[name]
    clients = []
    while True:
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            
            #建连接
            # logger.info("input connecting: " + ip + " " + str(port))
            sock.bind((ip, port))
            # logger.info("input connected: " + ip + " " + str(port))
            sock.listen(1)
            print("listen success ip",ip)
            print("listen success port", port)

            while True:
                _sock,_addr = sock.accept()
                logger.debug(name + ' ==> accept from :' + str(_addr))
                print('accept from', str(_addr))
                # time.sleep(10)
                while True:
                    packdata = _sock.recv(1024)
                    # packdata = readPackage(_sock)
                    print(packdata)
                    queue.put(packdata)

                    # print("recv data: packdata", packdata)
                    # 数据缓冲到队列
                    # if packdata:
                    #    global_data.append(packdata)
                    # 转发

        except Exception as e:
            logger.error(str(e))
        finally:
            sock.close()
            time.sleep(3)


def routineOutPut(name):
    ip = LOCAL_HOST
    port = OUTPUT_PORTS[name]
    logger.info("output routine " + name + " started, ip=" + ip + " port=" + str(port))

    sock_list = []
    queue = queDic[name]

    # threadDispatch = threading.Thread(target=routineDispatch, args=(name, sock_list))
    # threadDispatch.start()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    while True:  
        #等待连接
        _sock,_addr = sock.accept()
        logger.debug(name + ' ==> accept from :' + str(_addr))
        print('accept from: {}'.format(_addr))
        while True:
            # 转发数据
            # print('global_data',global_data)
            # for data in global_data:
                # if data:
                #    print("转发数据data", data)
                #   _sock.send(data)
            if not queue.empty():
                data = queue.get()
                print('Send data!')
                _sock.send(data)
            else:
                print('queue is empty!')
                break


        # #添加sock到sock_list
        # lock.acquire()
        # sock_list.append(_sock)
        # lock.release()



if __name__ == "__main__":
    logger.info("FACEWARE CENTER SERVER")

    #初始化队列资源
    for name, _ in INPUT_PORTS.items():
        queue = FrameQue()
        queDic[name] = queue

    #启动Input线程组
    for name, _ in INPUT_PORTS.items():
        threadInPut = threading.Thread(target=routineInPut, args=(name,))
        threadInPut.start()

    #启动Output线程组
    for name, _ in OUTPUT_PORTS.items():
        threadOutPut = threading.Thread(target=routineOutPut, args=(name,))
        threadOutPut.start()

