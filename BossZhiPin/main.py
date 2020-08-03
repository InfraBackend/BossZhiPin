from scrapy.cmdline import execute

import sys
import os   # 用来获取路径的模块

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'zhipin'])
