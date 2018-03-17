# -*- coding: UTF-8 -*-
import boto3
import botocore
import os

AWS_Profile='dymail'
BUCKET_NAME='log-auto-checkin-dy'

env_region=os.environ.get('region','us-east-1')
awsEnv=os.environ.get('AWS_ENV',0)
import logging
logger = logging.getLogger(__name__)

if awsEnv == "1":
    session = boto3.Session()
else:
    session = boto3.Session(profile_name='dymail')

def sendMail(Message):
    topicARN = 'arn:aws:sns:us-east-1:757977731860:qiandao'
    # topicARN = 'arn:aws:sns:us-east-1:757977731860:mobileSMS'
    # Create an SNS client
    if Message!='':
        client = session.client("sns",region_name=env_region)
        client.publish(TopicArn=topicARN, Message=Message)
    else:
        logger.error('Message is empty')


def uploadS3Bucket(File):
    s3=session.resource("s3",region_name=env_region)
    data = open(File, 'rb')
    s3Name=File.split('/')[-1].replace("_","/")
    s3.Bucket('log-auto-checkin-dy').put_object(Key=s3Name, Body=data)


def uploadS3Cookies(File):
    s3=session.resource("s3",region_name=env_region)
    data = open(File, 'rb')
    s3Name="cookies/"+File.split('/')[-1].replace("_","/")
    s3.Bucket('log-auto-checkin-dy').put_object(Key=s3Name, Body=data)

def downloadS3Cookies(File):
    s3=session.resource("s3",region_name=env_region)
    try:
        s3Name = "cookies/" + File.split('/')[-1].replace("_", "/")
        s3.Bucket(BUCKET_NAME).download_file(s3Name, File)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.error("The object %s does not exist."%s3Name)
            raise Exception
        else:
            logger.error("The object %s does not exist."%s3Name)
            raise Exception


if __name__ == '__main__':
    sendMail("this is a test mail from AWS")
    # uploadS3Bucket("/tmp/auto_qiandao_2018-03-11_14:48:52.log")
    # uploadS3Cookies("/tmp/auto_qiandao_2018-03-11_14:48:52.log")
    # downloadS3Cookies("/tmp/auto_qiandao_2018-03-11_14:48:52.log")
