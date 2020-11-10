import time

from ._compat import urlopen
from .exceptions import QencodeTaskException
from .task import Task


class Metadata(Task):
    def get(self, uri):
        params = (
            """
            {"query": {
              "source": "%s",
              "format": [ {"output": "metadata", "metadata_version": "4.1.5"} ]
              }
            }
            """
            % uri
        )
        self.custom_start(params)
        while True:
            status = self.status()
            # print status
            # print json.dumps(status, indent=2, sort_keys=True)
            if status['error'] or status['status'] == 'completed':
                break
            time.sleep(5)

        if self.error:
            raise QencodeTaskException(self.message)

        url = None
        if len(status['videos']) > 0:
            url = status['videos'][0]['url']
        elif len(status['audios']) > 0:
            url = status['audios'][0]['url']

        if url is None:
            raise QencodeTaskException('No metadata URL found in status response')

        data = urlopen(url).read()

        return data
