#coding: utf-8
import socket,struct
import datetime


#-------------------------------------------------------------------------------------
def opendump():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d%H%M%S')
    global dumpf
    dumpf = open('dump_'+ filename, 'ab+')


def writedump(data):
    global dumpf
    dumpf.write(data)


def closedump():
    dumpf.close()


#-------------------------------------------------------------------------------------

def recvAll(sock, len_recv):
    len_leave = len_recv
    data = b''

    while True:
        tmp = sock.recv(len_leave)
        len_recved = len(tmp)
        if 0 == len_recved:
            raise Exception("read io failed.")

        data += tmp
        len_leave = len_leave - len_recved
        if(0 == len_leave):
            break
    return data


#-------------------------------------------------------------------------------------

def readPackage(sock, flag_dump=False):
    head = recvAll(sock, 4)
    len_body = struct.unpack('<L', head[0:4])[0]
    body = recvAll(sock, len_body)

    packdata = str(head) + str(body)
    if flag_dump: 
        writedump(packdata)
    return packdata


#-------------------------------------------------------------------------------------

