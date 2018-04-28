import json
import boto3
import botocore
import os
import random
import tempfile
from twython import Twython, TwythonError

BUCKET_NAME = 'tajweedbot'
CONSUMER_KEY = 'eUuIASW0ruPI5WtVW8s2E8UOY'
CONSUMER_SECRET = 'fCz0aFmZ52fRQXzAYK5tvshj6ndz09ZJwhF68Mc7mzCR1uxd22'
ACCESS_TOKEN = '989882912953847808-5hnilvIOPNS7de0qnVy3ufuiVbvwukF'
ACCESS_SECRET = 'C5hlutKJDc0gALVJRZ7uPFxMbHenEo52PwWFmbUtoeuAJ'


s3 = boto3.resource('s3')
bucket= s3.Bucket(BUCKET_NAME)

obj = str(random.randint(1, sum(1 for _ in bucket.objects.all())))
KEY = obj + '.jpg'

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
            twitter.update_status(status="Today's Tajweed rule" , media_ids=twit_resp['media_id'])
            print("image tweeted")
        except TwythonError as e:
            print(e)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise


