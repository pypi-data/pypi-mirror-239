import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import List


def get_logger(file_name="run",
               name=None,
               append_path: List = None,
               backup_count=21):
    base_li = ["/data", "project", "logs", "dplog"]
    if append_path:
        base_li.extend(append_path)
    base_dir = os.path.join(*base_li)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    log_file = os.path.join(base_dir, "{}.log".format(file_name))

    new_formatter = '%(asctime)s [%(name)s][%(lineno)4s][%(levelname)7s] %(message)s'
    fmt = logging.Formatter(new_formatter)

    file_handle = TimedRotatingFileHandler(log_file, when='D', backupCount=backup_count)
    file_handle.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(file_handle)
    log.addHandler(console_handler)
    return log
