#coding: utf-8
import socket
from Logger import logger
from Public import readPackage


#################################################################################
SOURCE_HOST = '127.0.0.1'
SOURCE_PORT = 8001
#################################################################################



if __name__ == "__main__":

    logger.info("SOURCE_HOST: " + SOURCE_HOST)
    logger.info("SOURCE_PORT: " + str(SOURCE_PORT))

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((SOURCE_HOST, SOURCE_PORT))  #链接source
    logger.info("source connected.")

    pack_sn = 0
    while True:
        pack_data = readPackage(sock)
        print("pack[" + str(pack_sn) + "] recved. ")
        pack_sn += 1
