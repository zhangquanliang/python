# -*- coding: utf-8 -*-
import aiohttp
import asyncio


async def fetch(client):
    async with client.get('http://python.org') as resp:
        assert resp.status == 200   # 响应码
        return await resp.text()    # resp.text()  文档内容


async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())