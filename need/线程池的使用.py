# -*- coding: utf-8 -*-
import threadpool


def ThreadFun(arg):
    print(arg)


def main():
    device_list=[1,2,3,4]  # 需要处理的设备个数
    task_pool = threadpool.ThreadPool(8)  # 8是线程池中线程的个数
    request_list = []  # 存放任务列表
    # 首先构造任务列表
    for device in device_list:
        request_list.append(threadpool.makeRequests(ThreadFun,[device]))
    # 将每个任务放到线程池中，等待线程池中线程各自读取任务，然后进行处理，使用了map函数，不了解的可以去了解一下。
    map(task_pool.putRequest,request_list)
    # 等待所有任务处理完成，则返回，如果没有处理完，则一直阻塞
    task_pool.poll()


if __name__=="__main__":
    main()