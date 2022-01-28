import json
from studienprojekt_cv_rvv.constants.paths import CONFIG_PATH, DEFAULT_CONFIG_PATH, PROJECT_ROOT
import os

TFOD_API_INSTALL_DIRECTORY = 'tfod_api_install_directory'
PRETRAINED_MODELS_DIRECTORY = 'pretrained_models_directory'
TRAINED_MODELS_DIRECTORY = 'trained_models_directory'
PRETRAINED_MODEL_NAME = 'pretrained_model_name'
PRETRAINED_MODEL_DOWNLOAD_LINK = 'pretrained_model_download_link'
TRAINED_MODEL_NAME = 'trained_model_name'
DATASET_DEFINITIONS_PATH = 'dataset_definitions_path'
DATASET_IMAGES_PATH = 'dataset_images_path'
CONFIG_KEYS = [
    TFOD_API_INSTALL_DIRECTORY,
    PRETRAINED_MODELS_DIRECTORY,
    TRAINED_MODELS_DIRECTORY,
    PRETRAINED_MODEL_NAME,
    PRETRAINED_MODEL_DOWNLOAD_LINK,
    TRAINED_MODEL_NAME,
    DATASET_DEFINITIONS_PATH,
    DATASET_IMAGES_PATH
]


class ConfigReader:

    def __init__(self, config_path=None, config_keys=None, matcher_keys=None):
        if config_keys is None:
            config_keys = []

        self.config_path = config_path
        self.config_dict = {}
        self.cache = {}
        self.load_config()
        self.config_keys = config_keys
        self.matcher_keys = matcher_keys or config_keys

    def load_config(self):
        try:
            with open(self.config_path, 'r') as json_file:
                self.config_dict = json.load(json_file)
            # we clear cache on every file load
            # because the contents might have changed
            self.cache = {}
        except (IOError, TypeError):
            print('could not read config file')

    def read_raw_value(self, key):
        key_is_good = (key in self.config_keys) and (key in self.config_dict)
        return self.config_dict[key] if key_is_good else None

    def get_value(self, key):
        if not (key in self.cache):
            value = self.read_raw_value(key)
            self.cache[key] = self.replace_shortcut_consts(value, key)
        return self.cache[key]

    def replace_shortcut_consts(self, value, key):
        value = value.replace('${PROJECT_ROOT}', PROJECT_ROOT)
        matched = [s for s in self.matcher_keys if (f'${{{s}}}' in value)]
        for m in matched:
            if m == key:
                continue
            value = value.replace(f'${{{m}}}', self.get_value(m))
        return value


project_config_reader = None


def get_reader():
    global project_config_reader
    if not project_config_reader:
        if os.path.isfile(CONFIG_PATH):
            project_config_reader = ConfigReader(
                CONFIG_PATH, CONFIG_KEYS,
                [PRETRAINED_MODEL_NAME, TRAINED_MODEL_NAME]
            )
        elif os.path.isfile(DEFAULT_CONFIG_PATH):
            project_config_reader = ConfigReader(
                DEFAULT_CONFIG_PATH, CONFIG_KEYS,
                [PRETRAINED_MODEL_NAME, TRAINED_MODEL_NAME]
            )
        else:
            project_config_reader = ConfigReader()

    return project_config_reader
