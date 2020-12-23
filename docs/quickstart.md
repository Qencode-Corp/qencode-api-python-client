## Installation

**install sdk libraries from github**

````
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
pip install -r requirements.txt
python setup.py install
````

**install from pip**

````
sudo pip install qencode
````

**Usage**

````
import qencode

API_KEY = 'your-api-qencode-key'

QUERY = """
{"query": {
  "source": "https://nyc3.s3.qencode.com/qencode/samples/1080-sample.mov",
  "format": [
    {
      "output": "mp4",
      "size": "320x240",
      "video_codec": "libx264"
    }
  ]
  }
}
"""

client = qencode.client(API_KEY)
client.create()

task = client.create_task()
task.custom_start(QUERY)


````


**Documentation**

Documentation is available at <https://docs.qencode.com>