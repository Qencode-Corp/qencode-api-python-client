#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time
import json
from qencode import QencodeClientException, QencodeTaskException

#replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'

params = """
{"query": {
  "source": "https://qencode.com/static/1.mp4",
  "format": [
    {
      "output": "mp4",
      "size": "320x240",
      "video_codec": "libx264"
    }
  ]
  }
}
"""

def progress_changed_handler(status):
  if status['status'] != 'completed':
    print json.dumps(status, indent=2, sort_keys=True)


def task_completed_handler(status, task_token):
  print 'Completed task: %s' % task_token
  print json.dumps(status, indent=2, sort_keys=True)


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

  print 'The client created. Expire date: %s' % client.expire

  task = client.create_task()

  if task.error:
    raise QencodeTaskException(task.message)

  task.custom_start(params)

  if task.error:
    raise QencodeTaskException(task.message)

  print 'Start encode. Task: %s' % task.task_token

  # using callback methods
  task.progress_changed(progress_changed_handler)
  task.task_completed(task_completed_handler, task.task_token)

if __name__ == '__main__':
  start_encode()