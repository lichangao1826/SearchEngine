# 运行环境：dev/product
environ = 'product'

if environ == 'dev':
    from . import *
elif environ == 'product':
    from .production import *

PROJECT_NAME = 'SearchEngine'
