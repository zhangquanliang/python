# -*- coding: utf-8 -*-
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.basename(__file__)))
execute(["scrapy", "crawl", "esczj"])
print(os.path.dirname(__file__))