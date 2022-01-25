import json
from studienprojekt_cv_rvv.constants.paths import CONFIG_PATH, DEFAULT_CONFIG_PATH, PROJECT_ROOT
import os

TFOD_API_INSTALL_DIRECTORY = 'tfod_api_install_directory'


class ConfigReader:

    def __init__(self, config_path=None):
        self.config_path = config_path
        self.config_dict = {}
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as json_file:
                self.config_dict = json.load(json_file)
        except (IOError, TypeError):
            print('could not read config file')

    def read_raw_value(self, key):
        return self.config_dict[key] if (key in self.config_dict) else None

    def get_value(self, key):
        value = self.read_raw_value(key)
        return ConfigReader.replace_shortcut_consts(value)

    @staticmethod
    def replace_shortcut_consts(value):
        value = value.replace('${PROJECT_ROOT}', PROJECT_ROOT)
        return value


project_config_reader = None
if os.path.isfile(CONFIG_PATH):
    project_config_reader = ConfigReader(CONFIG_PATH)
elif os.path.isfile(DEFAULT_CONFIG_PATH):
    project_config_reader = ConfigReader(DEFAULT_CONFIG_PATH)
else:
    project_config_reader = ConfigReader()


def get_reader():
    return project_config_reader
