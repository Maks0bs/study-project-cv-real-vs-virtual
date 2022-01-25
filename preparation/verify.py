from studienprojekt_cv_rvv.constants.general import OS_LINUX, OS_WINDOWS, ENV_OS
from studienprojekt_cv_rvv.constants.paths import PREPARATION_PKG_PATH
from studienprojekt_cv_rvv.common import config
import os
import subprocess

VERIFY_TFOD_API_SCRIPT_WINDOWS = os.path.join(
    PREPARATION_PKG_PATH, 'verify_scripts', 'verify_tfod_api_installation.bat'
)
VERIFY_TFOD_API_SCRIPT_LINUX = os.path.join(
    PREPARATION_PKG_PATH, 'verify_scripts', 'verify_tfod_api_installation.sh'
)


def verify_tfod_api(system, tfod_api_path):
    script = \
        VERIFY_TFOD_API_SCRIPT_WINDOWS if system == OS_WINDOWS else VERIFY_TFOD_API_SCRIPT_LINUX
    args = [script, tfod_api_path]
    log_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'verify_log.txt')
    exitcode = None
    with open(log_filename, 'w+') as logfile:
        exitcode = subprocess.call(args, stdout=logfile, stderr=logfile)

    with open(log_filename, 'r') as logfile:
        last_line = logfile.readlines()[-1]

    success = (exitcode == 0) and ('OK' in last_line)

    if os.path.exists(log_filename):
        os.remove(log_filename)

    return success


def verify_pretrained_model():
    pass


if __name__ == '__main__':
    verify_tfod_api(ENV_OS, config.get_reader().get_value(TFOD_API_INSTALL_DIRECTORY))
    verify_pretrained_model()