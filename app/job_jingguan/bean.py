# -*- coding: UTF-8 -*-
from pyquery import PyQuery

from . import common
from .daka import Daka
from .common import find_value, RequestError
import logging
logger = logging.getLogger(__name__)

class Bean(Daka):
    job_name = '经管论坛会员页签到领经验'

    index_url = 'http://bbs.pinggu.org/'
    info_url = 'http://bbs.pinggu.org/home.php?mod=spacecp&ac=credit'
    sign_url = 'http://bbs.pinggu.org/plugin.php?id=dsu_paulsign:sign'
    real_sign_url = 'http://bbs.pinggu.org/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
    test_url = 'http://bbs.pinggu.org/member.php?mod=logging&action=login'
    login_url = test_url
    logger=logger

    def __init__(self, session):
        super().__init__(session)
        self.page_data = ''

    def is_signed(self):
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
                'qdsubject': u'今天签到了，啊哈哈',
                'todaysay': u'今天签到了，啊哈哈，好开心',
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

    def _get_token(self):
        html = self._get_page_data()
        pattern = r'token:\s*"(\d+)"'
        token = common.find_value(pattern, html)

        if not token:
            raise Exception('token 未找到.')

        return token

    def _get_page_data(self):
        if not self.page_data:
            self.page_data = self.session.get(self.index_url).text

        return self.page_data
