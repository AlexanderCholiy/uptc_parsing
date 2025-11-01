import os
from logging import DEBUG, INFO

from settings.config import CURRENT_DIR, DEBUG_MODE

BASE_DIR = os.path.join(CURRENT_DIR, '..')
LOG_DIR = os.path.join(BASE_DIR, 'log')
DATA_DIR = os.path.join(BASE_DIR, 'data')
PARSING_LOG_DIR = os.path.join(LOG_DIR, 'parsing')

DEFAULT_LOG_FILE = os.path.join(LOG_DIR, 'app.log')
DEFAULT_ROTATING_LOG_FILE = os.path.join(LOG_DIR, 'app', 'app.log')
DEFAULT_LOG_MODE = 4 if DEBUG_MODE else 1
DEFAULT_LOG_LEVEL = DEBUG if DEBUG_MODE else INFO

PORTAL_TP_LOG_FILE = os.path.join(PARSING_LOG_DIR, 'portal_tp.log')

os.makedirs(os.path.dirname(DEFAULT_ROTATING_LOG_FILE), exist_ok=True)
os.makedirs(PARSING_LOG_DIR, exist_ok=True)

PARSING_LOCK_FILE = os.path.join(DATA_DIR, 'lock', 'parsing_lock.lock')

os.makedirs(os.path.dirname(PARSING_LOCK_FILE), exist_ok=True)
