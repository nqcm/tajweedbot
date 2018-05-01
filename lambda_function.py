import boto3
import botocore
import os
import random
import tempfile
from twython import Twython, TwythonError

BUCKET_NAME = 'YOU-BUCKET-NAME'
CONSUMER_KEY = 'TWITTER-APP-CONSUMER-KEY'
CONSUMER_SECRET = 'TWITTER-APP-CONSUMER-SECRET'
ACCESS_TOKEN = 'ACCESS-TOKEN'
ACCESS_SECRET = 'ACCESS-SECRET'


s3 = boto3.resource('s3')
bucket= s3.Bucket(BUCKET_NAME)

def lambda_handler(event, context):

    obj = str(random.randint(1, sum(1 for _ in bucket.objects.all())))
    KEY = obj + '.png'

    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)


    tmp_dir = tempfile.gettempdir()
    path = os.path.join(tmp_dir, KEY)
    print("created directory at " + path)
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, path)
        print('file moved to temp directory')
        with open(path, 'rb') as img:
            try:
                twit_resp = twitter.upload_media(media=img)
                twitter.update_status(status="The best of you is he who learns the Quran and teaches it. ~ Prophet Muhammad SAW" , media_ids=twit_resp['media_id'])
                print("image tweeted")
            except TwythonError as e:
                print(e)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


