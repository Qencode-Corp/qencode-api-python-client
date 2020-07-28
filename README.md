## qencode-api-python-client

**install sdk libraries from github**

```
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
pip install -r requirements.txt
python setup.py install
```

**install from pip**

```
pip install --upgrade qencode
```

**Usage**

```
import qencode

client = qencode.client(API_KEY)
client.create()

task = client.create_task()
task.start(TRANSCODING_PROFILEID, VIDEO_URL)


#getting video metadata:
metadata = client.get_metadata(VIDEO_URL)

```

**Documentation**

Documentation is available at <https://docs.qencode.com>

**Description**

Inside this library, you will find sample code for creating [video transcoding](https://cloud.qencode.com/) tasks, launching encoding jobs, video clipping and receiving callbacks. Updates are posted on a regular basis and we are open to any improvements or suggestions you may have.

Some of the options Qencode offers for transcoding your videos at scale:

Resolution

- 8K
- 4K
- 1440p
- 1080p
- 720p
- 480p
- 360p
- 240

Features

- Thumbnails
- Watermarking
- VR / 360 Encoding
- Subtitles & Captions
- Create Clips
- Video Stitching
- S3 Storage
- Preview Images
- Custom Resolution
- Callback URLs
- Custom Presets
- Rotate
- Aspect Ratio
- Notifications
- Crop Videos

Transfer & Storage Options

- S3 Qencode
- AWS
- Google Cloud
- Backblaze
- Azure
- FTP
- HTTP(S)
- VPN
