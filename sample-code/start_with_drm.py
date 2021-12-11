#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os.path
import sys
import time

import qencode
from qencode import QencodeClientException, QencodeTaskException, cenc_drm, fps_drm

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'
DRM_USERNAME = 'my.ezdrm@email.com'
DRW_PASSWORD = 'your-ezdrm-password'

QUERY = """
{
  "query": {
    "format": [
      {
        "output": "advanced_dash",
        "stream": [
          {
            "video_codec": "libx264",
            "height": 360,
            "audio_bitrate": 128,
            "keyframe": 25,
            "bitrate": 950
          }
        ],
        "cenc_drm" : {cenc_drm}
      }
    ],
    "source": "https://nyc3.s3.qencode.com/qencode/bbb_30s.mp4"
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

    encryption_parameters, payload = cenc_drm(DRM_USERNAME, DRW_PASSWORD)
    # encryption_parameters, payload = fps_drm(DRM_USERNAME, DRW_PASSWORD)

    query = QUERY.replace('{cenc_drm}', json.dumps(encryption_parameters))

    task.custom_start(query)

    if task.error:
        raise QencodeTaskException(task.message)

    print 'Start encode. Task: %s' % task.task_token

    while True:
        status = task.extend_status()
        # print status
        print json.dumps(status, indent=2, sort_keys=True)
        if status['error'] or status['status'] == 'completed':
            break
        time.sleep(5)


if __name__ == '__main__':
    start_encode()
