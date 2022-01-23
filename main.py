from constants.cmd import *
from constants.general import MODE_DEFAULT
import argparse
from common.cmd import CmdArgumentExtractor
from constants.general import ENV_OS

# TODO: the jupyter notebook should load all necessary packages
#  (maybe except for detect that gets loaded dynamically)


class MainArgumentExtractor(CmdArgumentExtractor):

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            description='The main script to execute all other modules of this project'
        )
        full_arg_mode = CMD_ARGS[CMD_ARG_MODE][CMD_ARG_OPT_FULL]
        short_arg_mode = CMD_ARGS[CMD_ARG_MODE][CMD_ARG_OPT_SHORT]
        parser.add_argument(
            short_arg_mode, full_arg_mode,
            nargs='?', type=str,
            choices=list(CMD_ARG_MODE_VALUES_TO_MODE_MAP.keys()),
        )
        return parser


def get_kwargs_for_execute(extractor):
    args = {}
    mode_value = extractor.get_extracted_arg(CMD_ARG_MODE)
    if mode_value:
        args['mode'] = CMD_ARG_MODE_VALUES_TO_MODE_MAP[mode_value]

    return args


def execute(mode=MODE_DEFAULT):
    print(ENV_OS)


if __name__ == '__main__':
    args_extractor = MainArgumentExtractor()
    kwargs = get_kwargs_for_execute(args_extractor)
    execute(**kwargs)
