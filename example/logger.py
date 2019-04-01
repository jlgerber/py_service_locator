"""
logger.py

Implementations of logger. We have ColoredLogger and Logger
"""
from example.context import service_locator
from example.services import BaseLogger
from example.color_util import (ColorCM, printit)


__all__ = ("Logger", "BaseLogger")

class Logger(BaseLogger):
    """
    Baseic logger implementation. Nothing fancy.
    """
    def __init__(self, name):
        """
        set the name
        """
        self.name = name

    def debug(self, *args):
        """
        trivial debug impl
        """
        print "DEBUG | {} |".format(self.name), " ".join(args)

    def info(self, *args):
        """
        trivial info impl
        """
        print "INFO  | {} |".format(self.name), " ".join(args)

    def warn(self, *args):
        """
        trivial warn impl
        """
        print "WARN  | {} |".format(self.name), " ".join(args)


class ColorLogger(BaseLogger):
    """
    Colored logger implementation. Like Logger but in color.
    """
    def __init__(self, name):
        """
        set the name
        """
        self.name = name

    def debug(self, *args):
        """
        trivial debug impl
        """
        with ColorCM(printit, "blue") as colorm:
            colorm("DEBUG | {} |".format(self.name), *args)

    def info(self, *args):
        """
        trivial info impl
        """
        with ColorCM(printit, "green") as colorm:
            colorm("INFO  | {} |".format(self.name), " ".join(args))

    def warn(self, *args):
        """
        trivial warn impl
        """
        with ColorCM(printit, "red") as colorm:
            colorm("WARN  | {} |".format(self.name), " ".join(args))

