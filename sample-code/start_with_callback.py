#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os.path
import sys

import qencode
from qencode import QencodeClientException, QencodeTaskException

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)


# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'

# replace with your Transcoding Profile ID (can be found in your Project settings on
# Qencode portal)
TRANSCODING_PROFILEID = 'your-qencode-profile-id'

# replace with a link to your input video
VIDEO_URL = 'https://qencode.com/static/1.mp4'


def progress_changed_handler(status):
    if status['status'] != 'completed':
        print(json.dumps(status, indent=2, sort_keys=True))


def task_completed_handler(status, task_token):
    print('Completed task: %s' % task_token)
    print(json.dumps(status, indent=2, sort_keys=True))


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

    print('The client created. Expire date: %s' % client.expire)

    task = client.create_task()
    task.start_time = 0.0
    task.duration = 10.0

    if task.error:
        raise QencodeTaskException(task.message)

    task.start(TRANSCODING_PROFILEID, VIDEO_URL)

    if task.error:
        raise QencodeTaskException(task.message)

    print('Start encode. Task: %s' % task.task_token)

    # using callback methods
    task.progress_changed(progress_changed_handler)
    task.task_completed(task_completed_handler, task.task_token)


if __name__ == '__main__':
    start_encode()
