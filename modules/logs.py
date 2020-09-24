#!/usr/bin/python3

"""Logger module."""
import logging.handlers
from os import environ

CVFILOG = logging.getLogger('CVFI Log')
CVFILOG.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('[%(asctime)s] - [%(levelname)s] \t- '
                              '%(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(int(environ.get('CVFI_LOGLEVELCONSOLE')))

CVFILOG.addHandler(CONSOLE_HANDLER)
