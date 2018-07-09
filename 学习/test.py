# -*- coding: utf-8 -*-

import socket
from urllib.parse import unquote, quote


a = quote('张三')
print(a)
b = unquote(a)
print(b)