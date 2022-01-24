from constants.general import *
from constants.cmd import *
from constants.paths import *
import os

from main import MainArgumentExtractor
from .verify import verify_tfod_api, verify_pretrained_model
from common import config
from common.config import TFOD_API_INSTALL_DIRECTORY
import subprocess

INSTALL_TFOD_API_SCRIPT_WINDOWS = os.path.join(PREPARATION_PKG_PATH, 'install_tfod_api.bat')
INSTALL_TFOD_API_SCRIPT_LINUX = os.path.join(PREPARATION_PKG_PATH, 'install_tfod_api.sh')


class PreparationArgumentExtractor(MainArgumentExtractor):

    @staticmethod
    def get_parser():
        parser = super(PreparationArgumentExtractor, PreparationArgumentExtractor).get_parser()
        parser.description = \
            'Script which prepares the workspace for all other activities' \
            'like training, evaluation and object detection'

        full_arg_mode = CMD_ARGS[CMD_ARG_VERIFY][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_VERIFY][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str,
            choices=list(CMD_VERIFY_ARG_TO_VAL_MAP.keys()),
        )
        return parser

    def get_kwargs_for_execute(self):
        args = super().get_kwargs_for_execute()
        mode_verify = self.get_extracted_arg(CMD_ARG_VERIFY)
        if mode_verify:
            args['verify'] = CMD_VERIFY_ARG_TO_VAL_MAP[mode_verify]

        return args


def install_tfod_api(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    if (verify in [VERIFY_BEFORE, VERIFY_BOTH]) and verify_tfod_api(ENV_OS):
        return True

    if ENV_OS == OS_WINDOWS:
        print(config.get_reader().get_value(TFOD_API_INSTALL_DIRECTORY))
        # args = [INSTALL_TFOD_API_SCRIPT_WINDOWS, ]
        # process = subprocess.Popen()


    # depending on OS run corresponding func
    # in each such func run corresponding verification if necessary flags are set
    # check for exitcode of verify-scripts. If != 0 then we have error
    # and we proceed to install (before) or we cancel installation process (if error on after)



def load_pretrained_model():
    pass


def execute(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    print(mode, verify)
    install_tfod_api(mode, verify)


if __name__ == '__main__':
    args_extractor = PreparationArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)
