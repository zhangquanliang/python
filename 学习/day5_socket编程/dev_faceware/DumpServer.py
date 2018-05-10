#coding: utf-8
import threading,time
import socket,struct
from Logger import logger


######################################################
LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8001
DUMP_FILE  = "dump"
######################################################


global offset #第二帧位置偏移量


def readPackage(f):
    head = f.read(4)
    if len(head) != 4:
        print("read EOF")
        return None

    len_body = struct.unpack('<L', head[0:4])[0]
    body = f.read(len_body)
    if len(body) != len_body:
        print("read EOF")
        return None

    packdata = head + body
    return packdata


def routineWorker(sock):
    try:
        dumpf = open(DUMP_FILE, 'rb')

        while True:
            packdata = readPackage(dumpf)
            if None == packdata:       #已经到文件结尾
                logger.info("maybe end of the dumpfile, reloading now...")
                dumpf.seek(0, 0)  #从第二帧开始读数据帧
                logger.info("seeking offset in dumpfile: " + str(0))
                continue

            sock.sendall(packdata)
            time.sleep(0.032)
    except Exception as e:
        logger.warn("conn maybe broken: " + str(e))
    finally:
        sock.close()
        dumpf.close()



def routineDumpServer():
    server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_sock.bind((LOCAL_HOST, LOCAL_PORT))
    server_sock.listen(1)

    while True:
        logger.info('waiting for new connection...')
        sock,addr = server_sock.accept()
        print('new connection accepted from :',addr)

        threadWorker = threading.Thread(target=routineWorker, args=(sock,))
        threadWorker.setDaemon(True)
        threadWorker.start()



if __name__ == "__main__":

    logger.info("LOCAL_HOST: " + LOCAL_HOST)
    logger.info("LOCAL_PORT: " + str(LOCAL_PORT))
    logger.info("DUMP_FILE: " + DUMP_FILE)

    threadServer = threading.Thread(target=routineDumpServer)
    threadServer.start()
    threadServer.join()

