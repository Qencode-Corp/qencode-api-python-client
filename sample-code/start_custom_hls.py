#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os.path
import sys
import time

import qencode
from qencode import QencodeClientException, QencodeTaskException

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'

params = qencode.custom_params()

FORMAT = qencode.format()
STREAM = qencode.stream()
DESTINATION = qencode.destination()

# set your S3 access credentials here
# for more storage types see Destination object description: https://docs.qencode.com/#010_050
DESTINATION.url = "s3://s3-eu-west-2.amazonaws.com/qencode-test"
DESTINATION.key = "your-s3-key"
DESTINATION.secret = "your-s3-secret"

# stream object is specified for HLS or DASH outputs only.
# for MP4 or WEBM output set properties below in format object directly
STREAM.profile = "baseline"
STREAM.size = "320x240"
STREAM.audio_bitrate = 128


FORMAT.stream = [STREAM]
FORMAT.output = "advanced_hls"
FORMAT.destination = DESTINATION

# replace with a link to your input video
params.source = 'https://qencode.com/static/1.mp4'
params.format = [FORMAT]


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
