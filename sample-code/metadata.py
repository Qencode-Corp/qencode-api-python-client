#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

import qencode
from qencode import QencodeClientException

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

# replace with your API KEY (can be found in your Project settings on Qencode portal)
API_KEY = 'your-api-qencode-key'
VIDEO_URL = 'https://nyc3.s3.qencode.com/qencode/bbb_30s.mp4'

client = qencode.client(API_KEY)
if client.error:
    raise QencodeClientException(client.message)

print('The client created. Expire date: %s' % client.expire)

metadata = client.get_metadata(VIDEO_URL)
print('Metadata: ' + metadata)
