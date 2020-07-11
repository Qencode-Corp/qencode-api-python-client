# flake8: NOQA
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    string_types = (str, unicode)
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError, URLError
    from urlparse import urljoin
else:
    string_types = (str,)
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
