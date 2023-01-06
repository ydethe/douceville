import logging


class DVLogFormatter(logging.Formatter):
    def __init__(self, notime=False):
        if notime:
            fmt = "[%(levelname)s] - %(message)s"
        else:
            fmt = "[%(levelname)s] - %(asctime)s - L%(lineno)d@%(filename)s - %(message)s"

        super().__init__(fmt=fmt, datefmt=None, style="%")

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        # if record.levelno == logging.DEBUG:
        #     self._style._fmt = DVLogFormatter.dbg_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result
