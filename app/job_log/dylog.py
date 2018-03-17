# -*- coding: UTF-8 -*-
import logging

LOG_FILENAME = '/tmp/example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
logging.debug('This DEBUG should go to the log file')
logging.info('This INFO should go to the log file')

logger = logging.getLogger('jobs')
logger.debug("test")
logger.info('info')
