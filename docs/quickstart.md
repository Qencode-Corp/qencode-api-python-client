## Installation

**install sdk libraries from github**

````
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
pip install -r requirements.txt
python setup.py install
````

**Usage**

````
from qencode import encoder, task

encoder_obj = encoder(API_KEY, api_url=API_URL)
encoder_obj.create_encoder()

task_obj = task(encoder_obj.access_token, encoder_obj.connect)
task_obj.start(TRANSCODING_PROFILEID, VIDO_URL)

````


**Documentation**

Documentation is available at <https://docs.qencode.com>