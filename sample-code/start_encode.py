#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time
import json


API_KEY = '5a5db6fa5b4c5'
TRANSCODING_PROFILEID = '5a5db6fa5b8ac'
VIDO_URL = 'https://qa.qencode.com/static/1.mp4'
line = "-" * 80 + "\n"



def start_encode():
  """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: client object
  """
  print line
  client = qencode.client(API_KEY)
  if client.error:
   print 'Error: %s\n' % client.message
   raise SystemExit

  """
    :return: task object
  """
  task = client.create_task()
  task.start_time = 0.0
  task.duration = 10.0
  task.start(TRANSCODING_PROFILEID, VIDO_URL)
  if task.error:
    print 'Error: %s\n' % task.message
    raise SystemExit

  while True:
    status = task.status()
    try:
      print_status(status)
    except BaseException as e:
      print str(e)
    if status['error']:
      break
    if status['status'] == 'completed':
      break
    time.sleep(10)


def print_status(status):
  if not status['error'] and status['status'] != 'error':
    print "Status: {0} {1}%".format(status.get('status'), status.get('percent'))
  elif status['error'] or status['status'] == 'error':
    print "Error: %s\n" % (status.get('error_description'))
  if status['status'] == 'completed':
    print line
    for video in status['videos']:
      meta = json.loads(video['meta'])
      print 'Resolution: %s' % meta.get('resolution')
      print 'Url: %s' % video.get('url')
    print line


if __name__ == '__main__':
  start_encode()