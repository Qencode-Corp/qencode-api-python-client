#
CPIX_API_URL_V4 = 'https://cpix-integration.keyos.com/api/v4/getKeys'
LA_URL_V4       = 'https://widevine.keyos.com/api/v4/getLicense'

NSMAP = {
  'cpix': 'urn:dashif:org:cpix',
  'enc': 'http://www.w3.org/2001/04/xmlenc#',
  'pskc': 'urn:ietf:params:xml:ns:keyprov:pskc',
  'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
  'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

SYSTEM_ID_PLAYREADY = '9a04f079-9840-4286-ab92-e65be0885f95'
SYSTEM_ID_WIDEVINE  = 'edef8ba9-79d6-4ace-a3c8-27dcd51d21ed'
SYSTEM_ID_FAIRPLAY  = '94ce86fb-07ff-4f43-adb8-93d2fa968ca2'

TRACK_TYPES = [
  ('SD',     0),     # (<720p)
  ('HD',     720),   # (720p)
  ('FULLHD', 1080),  # (1080p)
  ('2KUHD',  1440),  # (1440p)
  ('4KUHD',  2160),  # (2160p)
  ('8KUHD',  4320),  # (4320p)
  ('16KUHD', 8640),  # (8640p)
]

DEFAULT_TRACK_TYPE = 'SD'
AUDIO_TRACK_TYPE   = 'AUDIO' # SD - old

