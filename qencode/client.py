from task import Task

from .httptools import Http
from .metadata import Metadata


class Client(object):
    def __init__(self, api_key, api_url=None, version=None):
        self.api_key = api_key
        self.api_url = api_url if api_url else 'https://api.qencode.com/'
        self.version = version if version else 'v1'
        self.connect = Http(self.version, self.api_url)
        self.access_token = None
        self.expire = None
        self.error = None
        self.code = None
        self.message = ''
        self._get_access_token()

    def create_task(self, **kwargs):
        return Task(self.access_token, self.connect, **kwargs)

    def refresh_access_token(self):
        response = self.connect.request('access_token', dict(api_key=self.api_key))
        if not response['error']:
            self.access_token = response['token']
            self.expire = response['expire']
        else:
            self.error = response['error']
            self.code = response['error']
            self.message = response.get('message')

    def _get_access_token(self):
        response = self.connect.request('access_token', dict(api_key=self.api_key))
        if not response['error']:
            self.access_token = response['token']
            self.expire = response['expire']
        else:
            self.error = response['error']
            self.code = response['error']
            self.message = response.get('message')

    def get_metadata(self, uri):
        metadata = Metadata(self.access_token, self.connect)
        video_info = metadata.get(uri)
        return video_info
