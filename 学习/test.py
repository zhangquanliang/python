# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool
import time


def say_hello(i):
    print('hello :{}'.format(i))
    time.sleep(2)


# 开启20个线程
start_time = time.time()
print(start_time)
pool = Pool(processes=20)
for i in range(101):
    pool.apply_async(say_hello, [i])
pool.close()
pool.join()
print('耗时：{}'.format(time.time() - start_time))