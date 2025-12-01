import base64
import json
import uuid
import time
import qencode
from qencode.drm.buydrm_v4 import create_cpix_user_request
from qencode import QencodeClientException, QencodeTaskException

# replace with your API KEY (can be found in your Project settings on Qencode portal)
# https://portal.qencode.com/
API_KEY = 'your-api-qencode-key'
# specify path to your BuyDRM certificate files, 
# for example create dir keys/ and put keys into
USER_PVT_KEY_PATH = 'keys/user-private_key.pem'
USER_PUB_CERT_PATH = 'keys/user-public_cert.pem'
# Qencode query template for job with {cpix_request}
query_json = 'query.json'
# correspond to stream resolution in query.json
key_ids = [
  { 'kid': str(uuid.uuid4()), 'track_type': 'SD' }, 
]
# need for BuyDRM
media_id = 'my asset' 
content_id = 'group21'
common_encryption = 'cenc'
# unified with the new BuyDRM API params
drm_list = {
  'PR': True, # use_playready
  'WV': True, # use_widevine
  'FP': False # use_fairplay
}
# for create log files: state-<token>.json, xml
debug = True

def start_encode():
  cpix_request = create_cpix_user_request(
    key_ids, media_id,
    content_id, common_encryption,
    USER_PVT_KEY_PATH, USER_PUB_CERT_PATH, #delivery_public_cert_path=None,  # if None - get from SDK, else - set public Qenocde certificate
    use_playready=drm_list['PR'], use_widevine=drm_list['WV'], use_fairplay=drm_list['FP']
  )

  client = qencode.client(API_KEY)
  if client.error:
    raise QencodeClientException(client.message)

  print('The client created. Expire date: %s' % client.expire)

  task = client.create_task()

  if task.error:
    raise QencodeTaskException(task.message)

  template = open(query_json, 'r').read()

  query = template.replace('{cpix_request}', base64.b64encode(cpix_request))

  task.custom_start(query)

  if task.error:
    raise QencodeTaskException(task.message)
  task_token = task.task_token
  print('Start encode. Task: %s' % task_token)

  while True:
    status = task.status()
    print('Job %s status: \n %s' % (task_token, json.dumps(status, indent=2, sort_keys=True)))
    if status['error'] or status['status'] == 'completed':
      break
    time.sleep(5)
  status = task.extend_status()
  print('Job %s finished with status "%s" and error: %s' % \
       (task_token, status['status'], status['error'])
  )
  if debug:
    open('job-cpix_request-%s.xml' % task_token, 'w').write(cpix_request)
    open('job-query-%s.json' % task_token, 'w').write(query)
    open('job-result-%s.json' % task_token, 'w').write(json.dumps(status, indent=2, sort_keys=True))

if __name__ == '__main__':
  start_encode()
