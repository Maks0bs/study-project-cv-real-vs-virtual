from constants.general import MODE_DEFAULT, VERIFY_DEFAULT
from constants.cmd import *
from main import MainArgumentExtractor
from verify import verify_tfod_api, verify_pretrained_model

# TODO: const which points to install bash and batch scripts


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


def install_tfod_api():
    pass
    # depending on OS run corresponding func
    # in each such func run corresponding verification if necessary flags are set
    # check for exitcode of verify-scripts. If != 0 then we have error
    # and we proceed to install (before) or we cancel installation process (if error on after)


def install_tfod_api_linux():
    pass


def install_tfod_api_windows():
    pass


def load_pretrained_model():
    pass


def execute(mode=MODE_DEFAULT, verify=VERIFY_DEFAULT):
    pass