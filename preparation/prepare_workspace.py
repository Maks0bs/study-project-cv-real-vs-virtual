import argparse
import subprocess
import sys
import os

from studienprojekt_cv_rvv.common import config
from studienprojekt_cv_rvv.common.cmd import CmdArgumentExtractor
from studienprojekt_cv_rvv.common.config import TFOD_API_INSTALL_DIRECTORY
from studienprojekt_cv_rvv.constants.cmd import *
from studienprojekt_cv_rvv.constants.general import *
from studienprojekt_cv_rvv.constants.paths import *
from verify import verify_tfod_api

INSTALL_TFOD_API_SCRIPT_WINDOWS = os.path.join(PREPARATION_PKG_PATH, 'install_tfod_api.bat')
INSTALL_TFOD_API_SCRIPT_LINUX = os.path.join(PREPARATION_PKG_PATH, 'install_tfod_api.sh')


class PreparationArgumentExtractor(CmdArgumentExtractor):

    @staticmethod
    def get_parser():
        description = \
            'Script which prepares the workspace for all other activities' +\
            'like training, evaluation and object detection'
        parser = argparse.ArgumentParser(
            description=description
        )
        full_arg_mode = CMD_ARGS[CMD_ARG_MODE][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_MODE][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str,
            choices=list(CMD_MODE_ARG_TO_VAL_MAP.keys()),
        )

        full_arg_mode = CMD_ARGS[CMD_ARG_VERIFY][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_VERIFY][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str,
            choices=list(CMD_VERIFY_ARG_TO_VAL_MAP.keys()),
        )
        return parser

    def get_kwargs_for_execute(self):
        args = {}
        mode_value = self.get_extracted_arg(CMD_ARG_MODE)
        if mode_value:
            args['mode'] = CMD_MODE_ARG_TO_VAL_MAP[mode_value]

        verify_value = self.get_extracted_arg(CMD_ARG_VERIFY)
        if verify_value:
            args['verify'] = CMD_VERIFY_ARG_TO_VAL_MAP[verify_value]

        return args


def install_tfod_api(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    tfod_api_path = config.get_reader().get_value(TFOD_API_INSTALL_DIRECTORY)
    # we check before if necessary and if tfod api is already installed
    # we don't need to do anything
    if (verify in [VERIFY_BEFORE, VERIFY_BOTH]) and verify_tfod_api(ENV_OS, tfod_api_path):
        return True
    # if not installed, we continue

    install_script = \
        INSTALL_TFOD_API_SCRIPT_WINDOWS if ENV_OS == OS_WINDOWS else INSTALL_TFOD_API_SCRIPT_LINUX

    args = [install_script, tfod_api_path]
    stdout = subprocess.DEVNULL if mode == MODE_SILENT else sys.stdout
    process = subprocess.Popen(args, stdout=stdout)
    _ = process.communicate()
    exitcode = process.returncode
    if exitcode != 0:
        raise subprocess.SubprocessError

    # check after installation if necessary (recommended)
    if verify in [VERIFY_AFTER, VERIFY_BOTH]:
        return verify_tfod_api(ENV_OS, tfod_api_path)

    # otherwise we assume everything was installed
    return True



def load_pretrained_model():
    pass


def execute(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    try:
        success = install_tfod_api(mode, verify)
        if not success:
            raise ValueError
    except (subprocess.SubprocessError, ValueError):
        if mode == MODE_VERBOSE:
            print('Installation of TFOD API failed')
        return


if __name__ == '__main__':
    args_extractor = PreparationArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)
