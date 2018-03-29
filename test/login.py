import aiohttp

response = aiohttp.request(method='get', url='https://www.baidu.com')
print(response.read())