import uuid
import time
import json
import base64
import qencode
from qencode.drm.buydrm import create_cpix_user_request
from qencode import QencodeClientException, QencodeTaskException

# replace with your API KEY (can be found in your Project settings on Qencode portal)
#API_KEY = 'your-api-qencode-key'
API_KEY = '5a2a846a26ace'
#API_KEY = '5a5db6fa5b4c5'

# specify path to your BuyDRM certificate files
USER_PVT_KEY_PATH = './keys/user_private_key.pem'
USER_PUB_CERT_PATH = './keys/user_public_cert.pem'

key_ids = [
  { 'kid': str(uuid.uuid4()), 'track_type': 'SD' },
  { 'kid': str(uuid.uuid4()), 'track_type': 'HD' }
]
media_id = 'my first stream'



QUERY = """
{
  "query": {
    "format": [
      {
        "output": "advanced_dash",
        "destination": {
          "url": "s3://nyc3.digitaloceanspaces.com/qencode3/regression_tests/encrypt/buydrm_widevine/dash",
          "key": "DRSKM355SM7QT4DB7Q37",
          "secret": "CGE1pypu02SfZ8DDPtZ5l1M5drFoVmAoVUrPBkQdAjM",
          "permissions": "public-read"
        },
        "stream": [
          {
            "video_codec": "libx264",
            "height": 360,
            "audio_bitrate": 128,
            "keyframe": 25,
            "bitrate": 950
          }
        ],
        "buydrm_drm": {
          "request": "{cpix_request}"
        }
      }
    ],
    "source": "https://nyc3.s3.qencode.com/qencode/bbb_30s.mp4"
  }
}
"""


def start_encode():
  # this creates signed request to BuyDRM
  cpix_request = create_cpix_user_request(
    key_ids, media_id, USER_PVT_KEY_PATH, USER_PUB_CERT_PATH,
    use_playready=True, use_widevine=True
  )

  #client = qencode.client(API_KEY, api_url='https://stage-sfo2-1-api-do.qencode.com/')
  #client = qencode.client(API_KEY, api_url='https://qa-sfo2-api-do.qencode.com/')
  client = qencode.client(API_KEY, api_url='https://prod-nyc1-api-do.qencode.com/')
  if client.error:
    raise QencodeClientException(client.message)

  print 'The client created. Expire date: %s' % client.expire

  task = client.create_task()

  if task.error:
    raise QencodeTaskException(task.message)

  query = QUERY.replace('{cpix_request}', base64.b64encode(cpix_request))

  task.custom_start(query)

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
