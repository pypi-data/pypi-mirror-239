import logging


class COLOR_FORMAT:
    RESET = '\033[0m'  # noqa
    NORMAL = ''  # noqa
    BOLD = '\033[01m'  # noqa
    FAINT = '\033[02m'  # noqa
    ITALIC = '\033[03m'  # noqa
    UNDERLINE = '\033[04m'  # noqa

    REVERSE = '\033[07m'  # noqa
    INVISIBLE = '\033[08m'  # noqa
    STRIKETHROUGH = '\033[09m'  # noqa


class COLOR_FOREGROUND:
    BLACK = '\033[30m'  # noqa
    RED = '\033[31m'  # noqa
    GREEN = '\033[32m'  # noqa
    YELLOW = '\033[33m'  # noqa
    BLUE = '\033[34m'  # noqa
    MAGENTA = '\033[35m'  # noqa
    CYAN = '\033[36m'  # noqa
    LIGHT_GRAY = '\033[37m'  # noqa
    GRAY = '\033[90m'  # noqa
    LIGHT_RED = '\033[91m'  # noqa
    LIGHT_GREEN = '\033[92m'  # noqa
    LIGHT_YELLOW = '\033[93m'  # noqa
    LIGHT_BLUE = '\033[94m'  # noqa
    LIGHT_MAGENTA = '\033[95m'  # noqa
    LIGHT_CYAN = '\033[96m'  # noqa
    WHITE = '\033[97m'  # noqa


class COLOR_BACKGROUND:  # noqa
    BLACK = '\033[40m'  # noqa
    RED = '\033[41m'  # noqa
    GREEN = '\033[42m'  # noqa
    YELLOW = '\033[43m'  # noqa
    BLUE = '\033[44m'  # noqa
    MAGENTA = '\033[45m'  # noqa
    CYAN = '\033[46m'  # noqa
    LIGHT_GRAY = '\033[47m'  # noqa
    GRAY = '\033[100m'  # noqa
    LIGHT_RED = '\033[101m'  # noqa
    LIGHT_GREEN = '\033[102m'  # noqa
    LIGHT_YELLOW = '\033[103m'  # noqa
    LIGHT_BLUE = '\033[104m'  # noqa
    LIGHT_MAGENTA = '\033[105m'  # noqa
    LIGHT_CYAN = '\033[106m'  # noqa
    WHITE = '\033[107m'  # noqa


LEVEL_TO_STYLE = {
    logging.CRITICAL: dict(
        foreground=COLOR_FOREGROUND.WHITE,
        background=COLOR_BACKGROUND.RED,
        format=COLOR_FORMAT.BOLD,
    ),
    logging.ERROR: dict(
        foreground=COLOR_FOREGROUND.RED,
        background=COLOR_BACKGROUND.BLACK,
    ),
    logging.WARNING: dict(
        foreground=COLOR_FOREGROUND.YELLOW,
        background=COLOR_BACKGROUND.BLACK,
    ),
    logging.INFO: dict(
        foreground=COLOR_FOREGROUND.GREEN,
        background=COLOR_BACKGROUND.BLACK,
    ),
    logging.DEBUG: dict(
        foreground=COLOR_FOREGROUND.WHITE,
        background=COLOR_BACKGROUND.BLACK,
        format=COLOR_FORMAT.FAINT,
    ),
    logging.NOTSET: dict(
        foreground=COLOR_FOREGROUND.WHITE,
        background=COLOR_BACKGROUND.BLACK,
    ),
}
