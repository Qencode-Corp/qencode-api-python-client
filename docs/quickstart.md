## Installation

**install sdk libraries from github**

```sh
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
pip install -r requirements.txt
python setup.py install
```

**install from pip**

```sh
sudo pip install qencode
```

**Usage**

```python
import qencode

client = qencode.client(API_KEY)
client.create()

task = client.create_task()
task.start(TRANSCODING_PROFILEID, VIDEO_URL)
```

**Documentation**

Documentation is available at <https://docs.qencode.com>
