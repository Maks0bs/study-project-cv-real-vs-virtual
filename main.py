from constants.cmd import *
from constants.general import MODE_DEFAULT
import argparse

# TODO: the jupyter notebook should load all necessary packages
#  (maybe except for object_detection that gets loaded dynamically)

# TODO: make another folder "common" where we will put all classes / fcts that are used
#  in all scripts / modules.
#  The CmdArgumentExtractor class should go there, as it will be used in every module
#  (in each module if __name__=='__main__' block to parse args and execute each module individually)


class CmdArgumentExtractor:

    def __init__(self, args=None):
        if not (args is None):
            self.args_dict = vars(self.get_parser().parse_args(args))
        else:
            self.args_dict = vars(self.get_parser().parse_args())

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

    def get_extracted_arg(self, arg):
        return self.args_dict[arg]


def get_kwargs_for_execute(extractor):
    args = {}
    mode_value = extractor.get_extracted_arg(CMD_ARG_MODE)
    if mode_value:
        args['mode'] = CMD_ARG_MODE_VALUES_TO_MODE_MAP[mode_value]

    return args


def execute(mode=MODE_DEFAULT):
    print(mode)


if __name__ == '__main__':
    args_extractor = CmdArgumentExtractor()
    kwargs = get_kwargs_for_execute(args_extractor)
    execute(**kwargs)
