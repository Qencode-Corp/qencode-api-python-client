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


def get_query_template():
    try:
        with open(
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'query.json'))
        ) as data:
            try:
                file_data = json.load(data)
                return json.dumps(file_data)
            except ValueError as e:
                print(e)
    except IOError as e:
        print(e)


params = get_query_template()


def start_encode():

    """
    Create client object
    :param api_key: string. required
    :param api_url: string. not required
    :param api_version: int. not required. default 'v1'
    :return: task object
    """

    client = qencode.Client(api_key=API_KEY)
    if client.error:
        raise QencodeClientException(client.message)

    print('The client created. Expire date: %s' % client.expire)

    task = client.create_task()

    if task.error:
        raise QencodeTaskException(task.message)

    task.custom_start(params)

    if task.error:
        raise QencodeTaskException(task.message)

    print('Start encode. Task: %s' % task.task_token)

    while True:
        status = task.status()
        # print status
        print(json.dumps(status, indent=2, sort_keys=True))
        if status['error'] or status['status'] == 'completed':
            break
        time.sleep(5)


if __name__ == '__main__':
    start_encode()
