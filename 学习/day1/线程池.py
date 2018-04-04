# -*- coding: utf-8 -*-
"""
threadpool 模块
pool = ThreadPool(poolsize)
requests = makeRequests(some_callable, list_of_args, callback)
[pool.putRequest(req) for req in requests]
pool.wait()
"""
import threadpool
import time
def sayhello(str):
    print("Hello ",str)
    time.sleep(2)
name_list =['xiaozi','aa','bb','cc']
start_time = time.time()
# pool = threadpool.ThreadPool(8) #8是线程池中线程的个数
# requests = threadpool.makeRequests(sayhello , name_list)
# [pool.putRequest(req) for req in requests]  # 将每个任务放到线程池中，等待线程池中线程各自读取任务，然后进行处理
# pool.wait()   # 等待所有任务处理完成，则返回，如果没有处理完，则一直阻塞
# pool.poll()
# print('%d second'% (time.time()-start_time))




