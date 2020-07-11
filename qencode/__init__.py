from .client import Client
from .custom_params import (
    CustomTranscodingParams,
    Destination,
    Format,
    Libx264_VideoCodecParameters,
    Libx265_VideoCodecParameters,
    Stream,
)
from .exceptions import QencodeClientException, QencodeTaskException


def client(api_key, api_url=None, version=None, **kwargs):
    from client import QencodeApiClient

    return Client(api_key, api_url=api_url, version=version, **kwargs)


__version__ = "1.0"
__status__ = "Production/Stable"
__author__ = "Qencode"
