#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time


API_KEY = '5a5db6fa5b4c5'
TRANSCODING_PROFILEID = '5a5db6fa5b8ac'
VIDO_URL = 'https://qa.qencode.com/static/1.mp4'



def start_encode():
  """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: client object
  """
  client = qencode.client(API_KEY)
  if client.error:
   print 'encoder error:', client.error, client.message
   raise SystemExit

  """
    :return: task object
  """
  task = client.create_task()
  task.start_time = 0.0
  task.duration = 10.0
  task.start(TRANSCODING_PROFILEID, VIDO_URL)
  if task.error:
    print 'task error:', task.error, task.message
    raise SystemExit

  while True:
    status = task.status()
    print '{0} | {1} | {2} | error: {3}'.format(VIDO_URL,
                                                status.get('status'),
                                                status.get('percent'),
                                                status.get('error'),
                                                status.get('error_description'))
    if status['error']:
      break
    if status['status'] == 'completed':
      break
    time.sleep(15)


if __name__ == '__main__':
   start_encode()