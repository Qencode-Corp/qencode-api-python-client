import base64
import json
import time
import uuid

import qencode
from qencode import QencodeClientException, QencodeTaskException
from qencode.drm.buydrm import create_cpix_user_request

# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'

# specify path to your BuyDRM certificate files
USER_PVT_KEY_PATH = './keys/user_private_key.pem'
USER_PUB_CERT_PATH = './keys/user_public_cert.pem'

key_ids = [
    {'kid': str(uuid.uuid4()), 'track_type': 'SD'},
    {'kid': str(uuid.uuid4()), 'track_type': 'HD'},
]
media_id = 'my first stream'


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
        key_ids,
        media_id,
        USER_PVT_KEY_PATH,
        USER_PUB_CERT_PATH,
        use_playready=True,
        use_widevine=True,
    )

    client = qencode.client(API_KEY)
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
