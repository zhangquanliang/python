# -*- coding:utf-8 -*-
"""
author = zhangql
"""

import asyncio
import requests
async def spider(loop):
    # run_in_exectuor会返回一个Future，而不是coroutine object
    future1 = loop.run_in_executor(None, requests.get, 'http://www.baidu.com/')
    future2 = loop.run_in_executor(None, requests.get, 'http://httpbin.org/')
    # 通过命令行可以发现上面两个网络IO在并发进行
    response1 = await future1  # 阻塞直到future1完成
    response2 = await future2  # 阻塞直到future2完成
    print(len(response1.text))
    print(len(response2.text))
    return 'done'
loop = asyncio.get_event_loop()
# If the argument is a coroutine object, it is wrapped by ensure_future().
result = loop.run_until_complete(spider(loop))
print(result)
loop.close()