import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.json')
DEFAULT_CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config_default.json')

PREPARATION_PKG_PATH = os.path.join(PROJECT_ROOT, 'preparation')
