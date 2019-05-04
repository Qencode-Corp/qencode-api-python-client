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
  "source": "https://qa.qencode.com/static/1.mp4",
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

  while True:
    status = task.status()
    # print status
    print json.dumps(status, indent=2, sort_keys=True)
    if status['error'] or status['status'] == 'completed':
      break
    time.sleep(5)

if __name__ == '__main__':
  start_encode()
