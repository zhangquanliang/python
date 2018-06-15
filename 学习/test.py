# -*- coding: utf-8 -*-
import requests
from openpyxl import Workbook

import requests

def get(i):
    if i==1:
        raise i
    else:
        print(i)

if __name__ == '__main__':
    for i in range(10):
        get(i)