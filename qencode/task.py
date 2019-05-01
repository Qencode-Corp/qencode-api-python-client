from custom_params import Query
from const import *
import time
import json
from utils import get_percent


class Task(object):
  def __init__(self, access_token, connect, debug=False, **kwargs):
    self.connect = connect
    self.status_url = None
    self.task_token = None
    self.access_token = access_token
    self._debug = debug
    self.message = ''
    self.error = None
    self.repeat = kwargs.get('repeats') if kwargs.get('repeats') else REPEAT



  def _prepare_data(self, profiles, video_url, **kwargs):
    data = dict(
      task_token=self.task_token,
      uri=video_url,
      profiles=', '.join(profiles) if type(profiles).__name__ == 'list' else profiles
    )
    if kwargs:
      data.update(kwargs)
    return data

  def _prepare_data2(self, query_json, **kwargs):
    data = dict(
      task_token=self.task_token,
      query=query_json
    )
    if kwargs:
      data.update(kwargs)
    return data


  def _create_task(self, count):
    res = self.connect.request('create_task', dict(token=self.access_token))
    if not res['error']:
      self.task_token = res.get('task_token')
    else:
      self.error = res['error']
      self.message = res.get('message')

    if self.error and self.error == 8:
      if count < REPEAT:
        time.sleep(SLEEP_ERROR)
        self._create_task(count + 1)

  def _start_encode(self, api_name, data):
    res = self.connect.request(api_name, data)
    if not res['error']:
      self.status_url = res.get('status_url')
    else:
      self.status_url = '{0}/{1}/status'.format(self.connect.url, self.connect.version)
      self.error = res['error']
      self.message = res.get('message')

  def _status(self):
    response = self.connect.post(self.status_url, dict(task_tokens=self.task_token))   
    if not response['error']:
        status = response['statuses'][self.task_token]
        if not status:
          status = self._status2()
        if status.get('status_url'):
          self.status_url = status.get('status_url')
        return status
    else:
      status = self._status2()
      return status


  def _status2(self):
    response = self.connect.request('status', {'task_tokens[]': self.task_token})    
    if not response['error']:
      res = response['statuses'][self.task_token]
      if res:
        if res.get('status_url'):
          self.status_url = res.get('status_url')
        return res
      else:
        return dict(error=True, message='Error getting status')
    else:
      return response




  def start(self, profiles, video_url, **kwargs):
    """Creating task and starting encode

      :param profiles: String or List object. Profile uuid
      :param transfer_method: String. Transfer method uuid
      :param video_url: String. Url of source video
      :param payload: String.
      :return: None

    """
    if not self.error:
      self._create_task(1)
      data = self._prepare_data(profiles, video_url, **kwargs)

      if not self.error and self.task_token:
        self._start_encode('start_encode', data)


  def custom_start(self, params,  **kwargs):
    """Creating task and starting encode

          :param query: JSON object for query param. For examples: https://docs.qencode.com
          :param payload: String.
          :return: None

    """
    if params is not None:
      query_obj = Query()
      query_obj.params = params
      query_obj.validate_params()
      if query_obj.error:
        self.error = query_obj.error
        self.message = query_obj.message
        return

      query_obj.prepare_params()
      if query_obj.error:
        self.error = query_obj.error
        self.message = query_obj.message

      if not self.error:
        self._create_task(1)
        data = self._prepare_data2(query_obj.query, **kwargs)

        if not self.error and self.task_token:
          self._start_encode('start_encode2', data)

    elif kwargs.get('query') is not None:
      query = kwargs.get('query')      
      if not self.error:
        self._create_task(1)
        data = self._prepare_data2(query, **kwargs)


        if not self.error and self.task_token:
          self._start_encode('start_encode2', data)
    else:
      self.error = True
      self.mesage = 'params or query is required'


  def status(self):
    """Getting status of encode from master-server.
        real time updating.

            :return: JSON object:
                {
                  'status' : 'encoding', 'percent': '50.90'  'error': 0 ...
                }

        """
    return self._status()

  def main_status(self):
    return self._status2()

  def progress_changed(self, callback, *args, **kwargs):
    while 1:
      status = self._status()
      if status['error']:
        return callback(status, *args, **kwargs)
      callback(status, *args, **kwargs)
      if status.get('status') in COMPLETED_STATUS:
        break
      time.sleep(SLEEP_REGULAR)


  def task_completed(self, callback, *args, **kwargs):
    while 1:
      status = self._status()
      if status['error']:
        return callback(status, *args, **kwargs)
      if status.get('status') in COMPLETED_STATUS:
        return callback(status, *args, **kwargs)
      if status.get('status') in COMPLETED_STATUS:
        break
      time.sleep(SLEEP_REGULAR)

