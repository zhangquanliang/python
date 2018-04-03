# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool
import time

def sayhello(str):
    print("Hello ",str)
    time.sleep(2)


def start_pool():
    start_time = time.time()
    pool = Pool(processes=10)
    for x in range(101):
        pool.map_async(sayhello, [x])
    pool.close()
    pool.join()
    print('%d second' % (time.time()-start_time))


if __name__ == '__main__':
    start_pool()