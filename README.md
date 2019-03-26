## qencode-api-python-client

####Installation

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

####Usage

````
from qencode import client

encode_obj = client.QencodeApiClient(API_KEY)
task = encoder_obj.create_task()
task.start(TRANSCODING_PROFILEID, VIDO_URL)

````

####Documentation

Documentation is available at <https://docs.qencode.com>