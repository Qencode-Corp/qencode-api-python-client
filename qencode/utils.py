import sys
import logging
import json

def is_number(s):
  try:
      float(s)
      return True
  except:
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
  for key, val in class_obj.__dict__.items():
    if not val:
      class_obj.__dict__.pop(key)

def rm_key_if_null(obj):
  if isinstance(obj, dict):
    return _rm_key(obj)
  elif isinstance(obj, str):
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
    if progress >= 1.:
      progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r{} [{}] {:.0f}% {}".format(message,
             "#" * block + "-" * (barLength - block), round(progress * 100, 0), status)
    sys.stdout.write(text)
    sys.stdout.flush()
    if self.task_completed:
      break

def log(self, path=None, name=None, log_format=None):
  format = '[%(asctime)s] %(levelname)s  %(message)s' if not log_format else log_format
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