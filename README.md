## qencode-api-python-client


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

````
#getting status

status = task.status()
or
status = task.extend_status()
````

````
#getting video metadata

metadata = client.get_metadata(VIDEO_URL)
````

**DRM** <sub><sup>*[details](https://docs.qencode.com/api-reference/transcoding/#start_encode2___query__attributes--format__attributes--fps_drm__attributes)*</sup></sub>

````
# getting Fairplay DRM encryption parameters
encryption_parameters, payload = cenc_drm(DRM_USERNAME, DRW_PASSWORD)

# getting Widevine and Playready DRM encryption parameters
encryption_parameters, payload = fps_drm(DRM_USERNAME, DRW_PASSWORD)

````


**AWS Signed URL**

````
source_url = generate_aws_signed_url(region, bucket, object_key, access_key, secret_key, expiration)

````

**Documentation**

Documentation is available at <https://docs.qencode.com>

**Description**

Inside this library, you will find sample code for creating [video transcoding](https://cloud.qencode.com/) tasks, launching encoding jobs, video clipping and receiving callbacks. Updates are posted on a regular basis and we are open to any improvements or suggestions you may have.

Some of the options Qencode offers for transcoding your videos at scale:

Resolution
 * 8K
 * 4K
 * 1440p 
 * 1080p 
 * 720p 
 * 480p 
 * 360p 
 * 240

Features 
 * Thumbnails 
 * Watermarking 
 * VR / 360 Encoding 
 * Subtitles & Captions 
 * Create Clips 
 * Video Stitching 
 * S3 Storage 
 * Preview Images 
 * Custom Resolution 
 * Callback URLs 
 * Custom Presets 
 * Rotate 
 * Aspect Ratio 
 * Notifications 
 * Crop Videos

Transfer & Storage Options
 * S3 Qencode
 * AWS 
 * Google Cloud 
 * Backblaze 
 * Azure 
 * FTP 
 * HTTP(S) 
 * VPN