##Usage

**Usage by transcoding profile ID**

````
from qencode import encoder, task
import time

API_KEY = 'Your Api Key'
TRANSCODING_PROFILEID = 'Your Profile ID'

VIDO_URL = 'Sourse Video Url'
API_URL = 'https://qa.qencode.com'


def start_encode():
  """
    Create encoder object
    :param api_key: string
    :param api_url: string. not required
    :return: encode object
  """
  encoder_obj = encoder(API_KEY, api_url=API_URL)
  encoder_obj.create_encoder()
  if encoder_obj.error:
   print 'encoder error:', encoder_obj.error, encoder_obj.message
   raise SystemExit

  """
    Create task
    :param access_token: string. access_token from encoder object
    :param connect: string. connect object from encoder object
    :return: task object
  """
  task_obj = task(encoder_obj.access_token, encoder_obj.connect)
  task_obj.start(TRANSCODING_PROFILEID, VIDO_URL)
  if task_obj.error:    
    raise SystemExit

  while True:
    status = task_obj.status()
    print status
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
from qencode import encoder, task, custom_params
import time

API_KEY = 'Your Api Key'
API_URL = 'https://qa.qencode.com'

format = custom_params.format
stream = custom_params.stream
destination = custom_params.destination
video_codec = custom_params.x264_video_codec
params = custom_params.base

destination.url = "s3://s3-eu-west-2.amazonaws.com/qencode-test"
destination.key = "AKIAIKZIPSJ7SDAIWK4A"
destination.secret = "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"

video_codec.vprofile = "baseline"
video_codec.level = 31
video_codec.coder = 0
video_codec.flags2 = "-bpyramid+fastpskip-dct8x8"
video_codec.partitions = "+parti8x8+parti4x4+partp8x8+partb8x8"
video_codec.directpred = 2

stream.size = "1920x1080"
stream.audio_bitrate = 128
stream.video_codec_parameters = video_codec

format.stream = [stream]
format.output = "advanced_hls"
format.destination = destination

params.source = 'https://qa.stagevids.com/static/1.mp4'
params.format = [format]



def start_encode():

  """
     Create encoder object
     :param api_key: string
     :param api_url: string. not required
     :return: encode object
   """
  encoder_obj = encoder(API_KEY, api_url=API_URL)
  encoder_obj.create_encoder()
  if encoder_obj.error:
    print 'encoder error:', encoder_obj.error, encoder_obj.message
    raise SystemExit

  """
      Create task
      :param access_token: string. access_token from encoder object
      :param connect: string. connect object from encoder object
      :return: task object
    """
  task_obj = task(encoder_obj.access_token, encoder_obj.connect)
  task_obj.custom_start(params)
  if task_obj.error:    
    raise SystemExit

  while True:
    status = task_obj.status()
    print status
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

task_obj.start(TRANSCODING_PROFILEID, VIDO_URL)
if task_obj.error:    
 raise SystemExit

task_obj.progress_changed(my_callback)
task_obj.task_completed(my_callback2)
````

**Documentation**

Documentation is available at <https://docs.qencode.com>
