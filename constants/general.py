from platform import system

# +-----------------+
# | Execution modes |
# +-----------------+

MODE_COLAB = 'mode_colab'
MODE_LOCAL = 'mode_local'
MODE_DEFAULT = MODE_LOCAL

# +----------------+
# | OS information |
# +----------------+

OS_WINDOWS = 'windows'
OS_LINUX = 'linux'
ENV_OS = system().lower()

