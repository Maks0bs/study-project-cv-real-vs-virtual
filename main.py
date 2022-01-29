import argparse

from studienprojekt_cv_rvv.common.cmd import CmdArgumentExtractor
from studienprojekt_cv_rvv.constants.cmd import *
from studienprojekt_cv_rvv.constants.general import MODE_DEFAULT
from studienprojekt_cv_rvv.setup import workspace as workspace_setup


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
            choices=list(CMD_MODE_ARG_TO_VAL_MAP.keys()),
        )
        return parser

    def get_kwargs_for_execute(self):
        args = {}
        mode_value = self.get_extracted_arg(CMD_ARG_MODE)
        if mode_value:
            args['mode'] = CMD_MODE_ARG_TO_VAL_MAP[mode_value]

        return args


def execute(mode=MODE_DEFAULT):
    if not workspace_setup.execute(mode=mode):
        # this get printed even if silent mode is active
        print('Workspace could not be set up')


if __name__ == '__main__':
    args_extractor = MainArgumentExtractor()
    kwargs = args_extractor.get_kwargs_for_execute()
    execute(**kwargs)
