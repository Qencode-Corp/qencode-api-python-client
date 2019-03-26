##Usage

**Usage by transcoding profile ID**

````
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time


API_KEY = 'Your API KEY'
TRANSCODING_PROFILEID = 'Your profile ID'
VIDO_URL = 'your source url'



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
````

**Usage by custom parameters**

````
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qencode
import time

API_KEY = 'Your API KEY'

params = qencode.custom_params()

FORMAT = qencode.format()
STREAM = qencode.stream()
DESTINATION = qencode.destination()
VIDEO_CODEC = qencode.x264_video_codec()


DESTINATION.url = "..."
DESTINATION.key = "..."
DESTINATION.secret = "..."

VIDEO_CODEC.vprofile = "baseline"
VIDEO_CODEC.level = 31
VIDEO_CODEC.coder = 0
VIDEO_CODEC.flags2 = "-bpyramid+fastpskip-dct8x8"
VIDEO_CODEC.partitions = "+parti8x8+parti4x4+partp8x8+partb8x8"
VIDEO_CODEC.directpred = 2

STREAM.profile = "baseline"
STREAM.size = "1920x1080"
STREAM.audio_bitrate = 128
STREAM.video_codec_parameters = VIDEO_CODEC

FORMAT.stream = [STREAM]
FORMAT.output = "advanced_hls"
FORMAT.destination = DESTINATION

params.source = 'your source url'
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
````
**Usage with callback methods**

````
def my_callback(e):
  print e

def my_callback2(e):
  print e
  
...

task.start(TRANSCODING_PROFILEID, VIDO_URL)
if task.error:    
 raise SystemExit

task.progress_changed(my_callback)
task.task_completed(my_callback2)
````

**Documentation**

Documentation is available at <https://docs.qencode.com>
