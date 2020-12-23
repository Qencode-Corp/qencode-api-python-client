#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time
import json
from qencode import QencodeClientException, QencodeTaskException
from qencode import generate_aws_signed_url

# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'

# request elements
region = 'us-east-2'
bucket = 'your-bucket-name'
object_key = 'path'
expiration = 86400  # time in seconds
access_key = 'your-AWS-access-key'
secret_key = 'your-AWS-secret-key'

# generate AWS signed url
source_url = generate_aws_signed_url(region, bucket, object_key, access_key, secret_key, expiration)
print(source_url)

format_240 = dict(
    output="mp4",
    size="320x240",
    video_codec="libx264"
)

format_720 = dict(
    output="mp4",
    size="1280x720",
    video_codec="libx264"
)

format = [format_240, format_720]

query = dict(
    source=source_url,
    format=format
)

params = dict(query=query)

def start_encode():

  """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: task object
  """


  client = qencode.client(API_KEY)
  if client.error:
    raise QencodeClientException(client.message)

  print('The client created. Expire date: {0}'.format(client.expire))

  task = client.create_task()

  if task.error:
    raise QencodeTaskException(task.message)

  task.custom_start(params)

  if task.error:
    raise QencodeTaskException(task.message)

  print('Start encode. Task: {0}'.format(task.task_token))

  line = "-"*80
  while True:
    print(line)
    status = task.status()
    # print status
    print(json.dumps(status, indent=2, sort_keys=True))
    if status['error'] or status['status'] == 'completed':
      break
    time.sleep(5)

if __name__ == '__main__':
  start_encode()
