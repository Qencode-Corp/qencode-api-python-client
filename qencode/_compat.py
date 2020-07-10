# flake8: NOQA
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    string_types = (str, unicode)
else:
    string_types = (str,)
