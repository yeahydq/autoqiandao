# -*- coding: UTF-8 -*-
import boto3
import jingguan
def run_job(event, context):
    jingguan.main()

if __name__ == '__main__':
    run_job(None,None)
