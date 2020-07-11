# Qencode Python Library

The Qencode Python library provides convenient access to the Qencode API
for applications written in the Python language.

Inside this repository in sample-code/, there are examples of [video transcoding](https://cloud.qencode.com/)
tasks, launching encoding jobs, video clipping and receiving callbacks. Updates are posted on a regular basis and we are open to any improvements or suggestions you may have.

## Installation

You don't need the source code unless you want to modify the package itself.
If you just want to use the package:

```sh
pip install --upgrade qencode
```

## Contributing

To modify the package, install [poetry](https://python-poetry.org/docs/#installation)
and checkout the source:

```sh
cd your-workspace-folder
git clone https://github.com/qencode-dev/qencode-api-python-client
cd qencode-api-python-client
poetry shell
poetry install
```

## Usage

```python
import qencode

client = qencode.Client(api_key=API_KEY)
client.create()

task = client.create_task()
task.start(TRANSCODING_PROFILEID, VIDEO_URL)

# Getting video metadata
metadata = client.get_metadata(VIDEO_URL)
```

## Documentation

Documentation is available at <https://docs.qencode.com>

## Features

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
