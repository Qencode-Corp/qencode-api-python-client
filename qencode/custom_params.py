import json
from json import JSONEncoder
from utils import rm_key_if_null

class CustomTranscodingParams(object):
  """CustomTranscodingParams

    :var source: String. Source video URI. Can be http(s) url or tus uri
    :var format: String. A list of objects, each describing params for a single output video stream (MP4, WEBM, HLS or MPEG-DASH)

  """
  def __init__(self):
    self.source = None
    self.format = None
    self.callback_url = None
    rm_key_if_null(self)

  def remove_null_params(self):
    rm_key_if_null(self)

class Format(object):
  """
      :var
      :var

    """
  def __init__(self):
    self.output = None
    self.file_extension = None
    self.destination = None
    self.segment_duration = None
    self.stream = None
    self.logo = None
    self.start_time = None
    self.duration = None
    self.is_watermark = None
    self.size = None
    self.video_codec = None
    self.audio_codec = None
    self.aspect_ratio = None
    self.quality = None
    self.interval = None
    self.width = None
    self.height = None
    self.time = None
    self.path = None
    self.resize_mod = None
    rm_key_if_null(self)

  def remove_null_params(self):
    rm_key_if_null(self)

class Destination(object):
  def __init__(self):
    self.url = None
    self.key = None
    self.secret = None
    self.permissions = None
    self.storage_class = None
    rm_key_if_null(self)

  def remove_null_params(self):
    rm_key_if_null(self)

class Stream(object):
  def __init__(self):
    self.size = None
    self.video_codec = None
    self.bitrate = None
    self.quality = None
    self.rotate = None
    self.framerate = None
    self.pix_format = None
    self.profile = None
    self.video_codec_parameters = None
    self.keyframe = None
    self.segment_duration = None
    self.start_time = None
    self.duration = None
    self.audio_bitrate = None
    self.audio_sample_rate = None
    self.audio_channels_number = None
    self.audio_codec = None
    self.downmix_mode = None
    self.logo = None
    self.aspect_ratio = None
    rm_key_if_null(self)

  def remove_null_params(self):
    rm_key_if_null(self)



class Libx264_VideoCodecParameters(object):
  def __init__(self):
    self.vprofile = None
    self.level = None
    self.coder = None
    self.flags2 = None
    self.partitions = None
    self.bf = None
    self.directpred = None
    self.me_method = None
    rm_key_if_null(self)

  def remove_null_params(self):
    rm_key_if_null(self)

class Libx265_VideoCodecParameters(object):
  def __init__(self):
    pass


class MyEncoder(JSONEncoder):
  def default(self, obj):
    return obj.__dict__


class Query(object):
  def __init__(self):
    self.params = None
    self.error = None
    self.message = ''
    self.query = None

  def prepare_params(self):
    query = dict(query=self.params)
    try:
      self.query = json.dumps(query, cls=MyEncoder, encoding='utf-8')
    except Exception as e:
      self.error = True
      self.message = repr(e)

  def validate_params(self):
    if not self.params:
      self.error = True
      self.message = 'for custom start encode - params is required'
      return
    if not 'source' in self.params.__dict__:
      self.error = True
      self.message = 'Params: source is required'
      return
    if not 'format' in self.params.__dict__:
      self.error = True
      self.message = 'Params: format is required'
      return
    for format in self.params.format:
      if not 'stream' in format.__dict__:
        self.error = True
        self.message = 'Params: stream is required in the format list'
        return
      if not 'output' in format.__dict__:
        self.error = True
        self.message = 'Params: output format is required in the format list'
        return
      for stream in format.stream:
        if not 'size' in stream.__dict__:
          self.error = True
          self.message = 'Params: size is required in the stream list'
          return


