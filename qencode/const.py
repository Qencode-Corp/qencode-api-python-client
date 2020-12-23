REPEAT = 32
SLEEP_REGULAR = 10
SLEEP_ERROR = 60
COMPLETED_STATUS = ['completed', 'saved']

ERROR_OK                = 0
ERROR_SERVER_INTERNAL   = 1
ERROR_BAD_APP_ID        = 2
ERROR_APP_ID_NOT_FOUND  = 3
ERROR_BAD_TOKEN         = 4
ERROR_TOKEN_NOT_FOUND   = 5
ERROR_TARIFF_NOT_PAID   = 6
ERROR_MASTER_NOT_FOUND  = 7
ERROR_SYSTEM_BUSY       = 8
ERROR_BAD_PAYLOAD       = 9
ERROR_PROJECT_NOT_FOUND = 10
ERROR_BAD_PROFILE       = 11
ERROR_PROFILE_NOT_FOUND = 12
ERROR_BAD_TOKENS        = 13
ERROR_FIELD_REQUIRED    = 14

FPS_DRM_KEYGENERATOR_URI_TEMPLATE = 'https://cpix.ezdrm.com/KeyGenerator/cpix.aspx?k=%s&u=%s&p=%s&c=resourcename&m=2'
CENC_DRM_KEYGENERATOR_URI_TEMPLATE = 'https://cpix.ezdrm.com/KeyGenerator/cpix.aspx?k=%s&u=%s&p=%s&c=resourcename&m=1'
DRM_KEY_URL_TEMPLATE = 'skd://fps.ezdrm.com/;%s'