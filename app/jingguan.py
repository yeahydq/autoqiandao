# -*- coding: UTF-8 -*-
import os
import sys
import pickle
import traceback
import requests

from config import config

import logging
import logging.config

GLOBAL_LOG_FORMAT = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
import time

GLOBAL_COOKIES_FILENAME='/tmp/jingguan_cookies'
# GLOBAL_LOG_FILENAME = '/tmp/auto_qiandao_%19s.log'%time.strftime("%Y-%m_%d_%H:%M:%S", time.localtime())
GLOBAL_LOG_FILENAME = '/tmp/auto_qiandao_2018-03_14_01:13:48.log'
try:
    os.remove(GLOBAL_COOKIES_FILENAME)
    os.remove(GLOBAL_LOG_FILENAME)
except Exception:
    pass


GLOBAL_LOG_LVL=logging.INFO

awsEnv=os.environ.get('AWS_ENV',0)

def set_logger():
    logging.basicConfig(format=GLOBAL_LOG_FORMAT, level=GLOBAL_LOG_LVL,filename=GLOBAL_LOG_FILENAME)
    logger = logging.getLogger(__name__)
    # logger.propagate = False
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(GLOBAL_LOG_FILENAME)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    formatter = logging.Formatter(GLOBAL_LOG_FORMAT)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


fh = logging.FileHandler(GLOBAL_LOG_FILENAME)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
logging.GLOBAL_LOG_FORMAT = GLOBAL_LOG_FORMAT
config_dict = {
     'handlers': {'fileHandler': {
                             'filename': 'blather_stat_cfg.log'
     }},
     'version': 1
}
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


from job_jingguan import ac_job_map
from aws.aws_mail import sendMail, uploadS3Bucket, uploadS3Cookies, downloadS3Cookies
# from job_log.logger import logger, GLOBAL_LOG_FILENAME, GLOBAL_COOKIES_FILENAME



def main(event, context):
    for ac in ac_job_map:
        jobs_all=ac_job_map[ac]
        logger.info("using %s "%ac)
        jobs = [job for job in jobs_all if job.__name__ not in config.jobs_skip]
        jobs_failed = []

        session = make_session(GLOBAL_COOKIES_FILENAME+"_"+ac)
        for job_class in jobs:
            job = job_class(session)

            try:
                job.run()
            except Exception as e:
                logger.error('# 任务运行出错: ' + repr(e))
                traceback.print_exc()

            if not job.job_success:
                jobs_failed.append(job.job_name)

        logger.info('=================================')
        logger.info('= 任务数: {}; 失败数: {}'.format(len(jobs), len(jobs_failed)))

        if jobs_failed:
            logger.error('= 失败的任务: {}'.format(jobs_failed))
        else:
            logger.info('= 全部成功 ~')

        logger.info('=================================')

        save_session(session,GLOBAL_COOKIES_FILENAME+"_"+ac)
    #
    # print('reading',GLOBAL_LOG_FILENAME)
    # print('size is %s' % os.path.getsize(GLOBAL_LOG_FILENAME))

    with open(GLOBAL_LOG_FILENAME, "r+") as f:
        sendMail(f.read())
        uploadS3Bucket(GLOBAL_LOG_FILENAME)


def make_session(GLOBAL_COOKIES_FILENAME) -> requests.Session:
    session = requests.Session()

    session.headers.update({
        'User-Agent': config.ua
    })

    try:
        downloadS3Cookies(GLOBAL_COOKIES_FILENAME)
        with open(GLOBAL_COOKIES_FILENAME, "rb") as f:
            cookies = pickle.load(f)
        session.cookies = cookies
        logging.info('# 从文件加载 cookies 成功.')
    except Exception as e:
        logging.error('# 未能成功载入 cookies, 要更新cookie~~ %s'%str(e))
        if awsEnv=="1":
            sys.exit(3)
    return session


def save_session(session,GLOBAL_COOKIES_FILENAME):
    with open(GLOBAL_COOKIES_FILENAME, "wb") as f:
        pickle.dump(session.cookies, f)

    uploadS3Cookies(GLOBAL_COOKIES_FILENAME)


# def proxy_patch():
#     """
#     Requests 似乎不能使用系统的证书系统, 方便起见, 不验证 HTTPS 证书, 便于使用代理工具进行网络调试...
#     http://docs.python-requests.org/en/master/user/advanced/#ca-certificates
#     """
#     import warnings
#     from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
#     class XSession(requests.Session):
#         def __init__(self):
#             super().__init__()
#             self.verify = False
#
#     requests.Session = XSession
#     warnings.simplefilter('ignore', InsecureRequestWarning)


if __name__ == '__main__':
    if config.debug and os.getenv('HTTPS_PROXY'):
        # proxy_patch()
        pass

    main(None, None)
