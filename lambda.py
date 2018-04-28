import json
import boto3
import botocore
import os
import random
from twython import Twython, TwythonError

BUCKET_NAME = 'tajweedbot'
KEY = 'round-zero.jpg'

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'local.jpg')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
