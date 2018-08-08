# -*- coding: UTF-8 -*-
from pyquery import PyQuery

from . import common
from .daka import Daka
from .common import find_value, RequestError
import logging
logger = logging.getLogger(__name__)
import urllib
import time
class Wenku(Daka):
    job_name = '百度签到领经验'

    # step 1/2 sign-in ( for chk the sign-in status)
    sign_url = 'https://wenku.baidu.com/task/submit/signin'
    # step 2/2 sign-in (sign in if step 1 is not sign-in yet)
    real_sign_url = 'http://bbs.pinggu.org/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'

    # to check whether it contain some unlogin info in the bucket
    test_url = 'https://wenku.baidu.com/task/submit/signin'
    test_url = 'https://wenku.baidu.com/user/mydocs?fr=nav'
    login_url = 'https://passport.baidu.com/v2/?login'
    logger=logger

    def __init__(self, session):
        super().__init__(session,self.login_url,self.test_url)
        self.page_data = ''

    def run(self):
        self.logger.info('Job Start: {}'.format(self.job_name))

        is_login = self.is_login
        self.logger.info('登录状态: {}'.format(is_login))

        if not is_login:
            self.logger.info('进行登录...')
            try:
                self.logger.info(self.login())
                # self.login()
                is_login = True
                self.logger.info('登录成功')
            except Exception as e:
                self.logger.error('登录失败: {}'.format(repr(e)))

        if is_login:
            if self.is_signed():
                self.job_success = True
            else:
                self.job_success = self.sign()

        self.logger.info('Job End.')

    @property
    def is_login(self):
        r = self.session.get(self.test_url, allow_redirects=False)
        # r = self.session.get(self.test_url)

        # if fail, location=http://passport.pinggu.org/login/index?appId=1&redirect=http%3A%2F%2Fbbs.pinggu.org
        # if 'errno' in r.text:
        #     return False
        # else:
        #     return True
        if r.is_redirect and 'passport' in r.headers.get('location',""):
            return False
        else:
            return True

    def is_signed(self):
        sign_url='https://wenku.baidu.com/task/submit/signin'
        page_data=self.session.get(self.sign_url).text

        data={
            'pid': '1',
            'bid': '1',
            'fr': '4',
            'act_id': '100369',
            'url': 'https://wenku.baidu.com/task/browse/daily',
            # 'refer': 'https://wenku.baidu.com/task/browse/daily',
            'refer': '',
            't': int(time.time())*1000,
            'index': '1',
            'ssl': '1',
            '_click_param_pc_rec_doc_2017_testid': '5',
            '_sessionx_url_param': '{}',
                }
        url='https://wkctj.baidu.com/click.gif'
        data = urllib.parse.urlencode(data)  # 提交类型不能为str，需要为byte类型
        # page_data = self.session.get(url,data=data)
        url='%s%s%s' % (url,'?',data)
        print(url)
        page_data = self.session.get(url)

        sign_url='https://wenku.baidu.com/task/submit/signin'
        page_data=self.session.get(self.sign_url).text
        signed = '今天可获得经验' not in PyQuery(page_data)('.biaoge').text()
        message1=PyQuery(page_data)('.luntanbi .biaoge .qdnewinfo').text()
        message2=PyQuery(page_data)('.qdnewbox_title').text()
        self.logger.info(message1)
        self.logger.info(message2)

        return signed

    def sign(self):
        # response = self.session.get(self.sign_url, params=payload).json()
        page_data=self.session.get(self.sign_url).text
        formhash = PyQuery(page_data)('.userli03 a').attr('href').split('=')[-1]

        requestForm={
                'formhash': formhash,
                'qdxq': 'kx',
                'qdmode': '1',
                'qdtypeid': '0',
                'qdsubject': '今天签到了，啊哈哈',
                'todaysay': '今天签到了，啊哈哈，好开心',
                'fastreply': '0',
                }

        r = self.session.post(self.real_sign_url,data=requestForm)
        # print(r.content)
        try:
            result = PyQuery(r.content.decode('gbk').encode('utf-8'))('.f_c .c').text()
            self.logger.info(result)

        except ValueError:
            raise RequestError('unexpected response: url: {}; http code: {}'.format(self.real_sign_url, r.status_code), response=r)

        if '成功' in result:
            # 签到成功, 获得若干个经验
            page_data = self.session.get(self.sign_url).text
            message = PyQuery(page_data)('.luntanbi .biaoge .qdnewinfo').text()
            self.logger.info(message)
            return True

        else:
            # 例如: 您已签到过，请勿重复签到！
            message = 'Fail'
            self.logger.error('签到失败: {}'.format(message))
            return False
    #
    # def _get_token(self):
    #     html = self._get_page_data()
    #     pattern = r'token:\s*"(\d+)"'
    #     token = common.find_value(pattern, html)
    #
    #     if not token:
    #         raise Exception('token 未找到.')
    #
    #     return token
    #
    # def _get_page_data(self):
    #     if not self.page_data:
    #         self.page_data = self.session.get(self.index_url).text
    #
    #     return self.page_data
