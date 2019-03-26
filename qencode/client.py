from httptools import Http
from task import Task

class QencodeApiClient(object):

  """
      :return: encoder object

  """
  def __init__(self, api_key, api_url=None, version=None, **kwargs):
    self.api_key = api_key
    self.api_url = api_url if api_url else 'https://api-qa.qencode.com' # 'https://api.qencode.com/'
    self.version = version if version else 'v1'
    self.connect = Http(self.version, self.api_url)
    self.access_token = None
    self.error = None
    self.message = ''


  def create(self):
    response = self.connect.request('access_token', dict(api_key=self.api_key))
    if not response['error']:
      self.access_token = response['token']
    else:
     self.error = response['error']
     self.message = response.get('message')

  def create_task(self, **kwargs):
    return Task(self.access_token, self.connect, **kwargs)
