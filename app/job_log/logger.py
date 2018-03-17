# -*- coding: UTF-8 -*-
import logging
GLOBAL_LOG_FORMAT = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
import time

GLOBAL_COOKIES_FILENAME='/tmp/jingguan_cookies'
GLOBAL_LOG_FILENAME = '/tmp/auto_qiandao_%19s.log'%time.strftime("%Y-%m_%d_%H:%M:%S", time.localtime())
GLOBAL_LOG_LVL=logging.INFO

# logging.basicConfig(level=GLOBAL_LOG_LVL)
logging.basicConfig(format=GLOBAL_LOG_FORMAT, level=GLOBAL_LOG_LVL,filename=GLOBAL_LOG_FILENAME)

logger = logging.getLogger('')
