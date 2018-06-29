# -*- coding: utf-8 -*-

import socket

print(socket.gethostname())

from os import popen
a = popen('hostname').read()
print(a)