import json
import time

from . import const as constants
from ._compat import string_types
from .custom_params import CustomTranscodingParams, Query
from .utils import is_json, rm_key_if_null


class Task(object):
    def __init__(self, access_token, connect, debug=False, **kwargs):
        self.connect = connect
        self.status_url = None
        self.main_status_url = '{0}/{1}/status'.format(
            self.connect.url, self.connect.version
        )
        self.task_token = None
        self.upload_url = None
        self.access_token = access_token
        self._debug = debug
        self.message = ''
        self.error = None
        self.repeat = (
            kwargs.get('repeats') if kwargs.get('repeats') else constants.REPEAT
        )
        self._create_task(1)

    def start(self, profiles, video_url, **kwargs):
        """Creating task and starting encode.

        :param profiles: String or List object. Profile uuid
        :param transfer_method: String. Transfer method uuid
        :param video_url: String. Url of source video
        :param payload: String.
        :return: None
        """
        if not self.error:
            # self._create_task(1)
            data = self._prepare_data(profiles, video_url, **kwargs)

            if not self.error and self.task_token:
                self._start_encode('start_encode', data)

    def custom_start(self, data, **kwargs):
        """Creating task and starting encode

        :param query: 
            JSON object for query param. For examples: https://docs.qencode.com
        :param payload: String.
        :return: None
        """
        if data is None:
            self.error = True
            self.message = 'Params is required'

        # if not self.error:
        #  self._create_task(1)

        if not self.error:
            query = self._prepare_query(data)

            if not self.error:
                data = self._prepare_data_custom(query, **kwargs)

        if not self.error and self.task_token:
            self._start_encode('start_encode2', data)

    def status(self):
        return self._status()

    def main_status(self):
        return self._status2()

    def progress_changed(self, callback, *args, **kwargs):
        while 1:
            status = self._status()
            if status['error']:
                return callback(status, *args, **kwargs)
            callback(status, *args, **kwargs)
            if status.get('status') in constants.COMPLETED_STATUS:
                break
            time.sleep(constants.SLEEP_REGULAR)

    def task_completed(self, callback, *args, **kwargs):
        while 1:
            status = self._status()
            if status['error']:
                return callback(status, *args, **kwargs)
            if status.get('status') in constants.COMPLETED_STATUS:
                return callback(status, *args, **kwargs)
            if status.get('status') in constants.COMPLETED_STATUS:
                break
            time.sleep(constants.SLEEP_REGULAR)

    def _prepare_query(self, params):
        if isinstance(params, CustomTranscodingParams):
            query_obj = Query()
            query_obj.params = params
            query_obj.validate_params()
            if query_obj.error:
                self.error = query_obj.error
                self.message = query_obj.message
            query_obj.prepare_params()
            if query_obj.error:
                self.error = query_obj.error
                self.message = query_obj.message
            return query_obj.query

        if isinstance(params, dict):
            query = rm_key_if_null(params)
            return json.dumps(query)

        if isinstance(params, string_types):
            if is_json(params):
                query = rm_key_if_null(params)
                return query
            else:
                self.error = True
                error_msg = "JSON is not well formatted"
                try:
                    self.message = "{}: {} Is not defined".format(error_msg, params)
                except Exception:
                    pass
                finally:
                    self.message = error_msg

    def _prepare_data(self, profiles, video_url, **kwargs):
        data = dict(
            task_token=self.task_token,
            profiles=', '.join(profiles)
            if type(profiles).__name__ == 'list'
            else profiles,
        )
        if isinstance(video_url, list):
            try:
                data.update(stitch=json.dumps(video_url))
            except Exception:
                data.update(stitch=video_url)
        else:
            data.update(uri=video_url)
        if kwargs:
            data.update(kwargs)
        return data

    def _prepare_data_custom(self, query_json, **kwargs):
        data = dict(task_token=self.task_token, query=query_json)
        if kwargs:
            data.update(kwargs)
        return data

    def _create_task(self, count):
        res = self.connect.request('create_task', dict(token=self.access_token))
        if not res['error']:
            self.task_token = res.get('task_token')
            self.upload_url = res.get('upload_url')
        else:
            self.error = res['error']
            self.message = res.get('message')

        if self.error and self.error == 8:
            if count < constants.REPEAT:
                time.sleep(constants.SLEEP_ERROR)
                self._create_task(count + 1)

    def _start_encode(self, api_name, data):
        res = self.connect.request(api_name, data)
        if not res['error'] and res.get('status_url'):
            self.status_url = res['status_url']
        else:
            self.status_url = self.main_status_url
            self.error = res.get('error')
            self.message = res.get('message')

    def _status(self):
        response = self.connect.post(self.status_url, dict(task_tokens=self.task_token))
        status = None

        if response['error'] == constants.ERROR_BAD_TOKENS:
            raise ValueError('Bad token: ' + str(self.task_token))

        if 'statuses' in response and self.task_token in response['statuses']:
            status = response['statuses'][self.task_token]

        if not status and self.status_url != self.main_status_url:
            self.status_url = self.main_status_url
            response = self.connect.post(
                self.status_url, dict(task_tokens=self.task_token)
            )
            if 'statuses' in response and self.task_token in response['statuses']:
                status = response['statuses'][self.task_token]

        if status and 'status_url' in status:
            self.status_url = status['status_url']

        return status
