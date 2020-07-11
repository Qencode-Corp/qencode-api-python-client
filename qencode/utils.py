import json
import logging
import sys

from ._compat import string_types


def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False


def get_percent(p):
    if is_number(p):
        return round(p)
    return 0


def is_json(value):
    try:
        json.loads(value)
    except ValueError:
        return False
    return True


def rm_attributes_if_null(class_obj):
    attrs = list(key for key in class_obj.__dict__.keys() if not key.startswith('__'))
    for attr in attrs:
        if getattr(class_obj, attr, None) is None:
            delattr(class_obj, attr)


def rm_key_if_null(obj):
    if isinstance(obj, dict):
        return _rm_key(obj)
    elif isinstance(obj, string_types):
        res = _rm_key(json.loads(obj))
        return json.dumps(res)


def _rm_key(_dict):
    for key, val in _dict.items():
        if not val:
            _dict.pop(key)
    return _dict


def progress_bar(self, custom_message=None):
    message = custom_message if custom_message else ''
    while 1:
        barLength, status = 20, ""
        progress = float(self.percent) / 100.0
        if progress >= 1.0:
            progress, status = 1, "\r\n"
        block = int(round(barLength * progress))
        text = "\r{} [{}] {:.0f}% {}".format(
            message,
            "#" * block + "-" * (barLength - block),
            round(progress * 100, 0),
            status,
        )
        sys.stdout.write(text)
        sys.stdout.flush()
        if self.task_completed:
            break


def log(self, path=None, name=None, log_format=None):
    format = (
        '[%(asctime)s] %(levelname)s  %(message)s' if not log_format else log_format
    )
    name = name if name else '{0}.log'.format(self.task.token)
    path = path if path else ''
    log_name = '{0}{1}'.format(path, name)
    logging.basicConfig(filename=log_name, format=format())
    logging.getLogger().setLevel(logging.INFO)
    log = logging.getLogger()
    while 1:
        log.info('{0} | {1} | {2}'.format(self.status, self.percent, self.message))
        if self.task_completed:
            break


def get_tus_from_url(url=''):
    try:
        if url.find('tus:') == 0:
            return url
        else:
            x = url.split('/')[-1]
            if x == url:
                return url
            else:
                return 'tus:' + x
    except Exception:
        return url
