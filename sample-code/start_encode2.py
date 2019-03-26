#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time

API_KEY = '5a5db6fa5b4c5'

params = qencode.custom_params()

FORMAT = qencode.format()
STREAM = qencode.stream()
DESTINATION = qencode.destination()
VIDEO_CODEC = qencode.x264_video_codec()


DESTINATION.url = "s3://s3-eu-west-2.amazonaws.com/qencode-test"
DESTINATION.key = "AKIAIKZIPSJ7SDAIWK4A"
DESTINATION.secret = "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"
DESTINATION.remove_null_params()

VIDEO_CODEC.vprofile = "baseline"
VIDEO_CODEC.level = 31
VIDEO_CODEC.coder = 0
VIDEO_CODEC.flags2 = "-bpyramid+fastpskip-dct8x8"
VIDEO_CODEC.partitions = "+parti8x8+parti4x4+partp8x8+partb8x8"
VIDEO_CODEC.directpred = 2
VIDEO_CODEC.remove_null_params()

STREAM.profile = "baseline"
STREAM.size = "1920x1080"
STREAM.audio_bitrate = 128
STREAM.video_codec_parameters = VIDEO_CODEC
STREAM.remove_null_params()

FORMAT.stream = [STREAM]
FORMAT.output = "advanced_hls"
FORMAT.destination = DESTINATION
FORMAT.remove_null_params()

params.source = 'https://qa.qencode.com/static/1.mp4'
params.format = [FORMAT]


def start_encode():

  """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: client object
  """
  client = qencode.client(API_KEY)
  client.create()
  if client.error:
    print 'encoder error:', client.error, client.message
    raise SystemExit

  """
    Create task
    :return: task object
  """

  task = client.create_task()
  task.custom_start(params)
  if task.error:
    print 'task error:', task.error, task.message
    raise SystemExit

  while True:
    status = task.status()
    print '{0} | {1} | {2} | error: {3}'.format(params.source,
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
