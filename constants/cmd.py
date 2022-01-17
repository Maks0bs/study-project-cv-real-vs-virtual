from .general import MODE_LOCAL as _MODE_LOCAL, MODE_COLAB as _MODE_COLAB

# +--------------------+
# | Common definitions |
# +--------------------+

CMD_ARG_OPT_FULL = 'full'
CMD_ARG_OPT_SHORT = 'short'

# +------------------------------------+
# | Command line arguments and options |
# +------------------------------------+

CMD_ARG_MODE = 'mode'

CMD_ARGS = {
    CMD_ARG_MODE: {
        CMD_ARG_OPT_FULL: '--mode',
        CMD_ARG_OPT_SHORT: '-m'
    }
}

CMD_ARG_MODE_VALUES_TO_MODE_MAP = {
    'colab': _MODE_COLAB,
    'local': _MODE_LOCAL
}