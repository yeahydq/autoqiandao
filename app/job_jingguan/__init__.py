# -*- coding: UTF-8 -*-
import logging

from .bean import Bean
from .baiduwenku import Wenku

# from .baidu.bean import Bean as baiduwenku

# jobs_web = [Bean]
jingguan_jobs_all = [Bean]

# baidu_jobs = [baiduwenku]
# baidu_all = baidu_jobs
baidu_jobs_all = [Wenku]

ac_job_map={
    # # 经管:
    # 'yeahydq1':jingguan_jobs_all,
    # # '13539999344': jobs_all,
    # '17322052018': jingguan_jobs_all,

    # 百度:
    'wenku_yeahydq':baidu_jobs_all,

}
