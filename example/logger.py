"""
logger.py

Implementations of logger. We have ColoredLogger and Logger
"""
from example.context import service_locator
from example.services import BaseLogger
from example.color_util import (ColorCM, printit)
import os

__all__ = ("Logger", "EnvLogger", "ColorLogger", "EnvColorLogger")

LEVELS = {"debug": 10, "info" : 20, "warn": 30}
def lookup_level(level):
    if isinstance(level, int):
        return level
    return LEVELS.get(level,10)

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


class EnvLogger(BaseLogger):
    """
    Baseic logger implementation. Adds ability to look up logging level from env
    using LOGGING_LEVEL env var.
    """
    def __init__(self, name, level=os.environ.get("LOGGING_LEVEL", "debug")):
        """
        set the name
        """
        self.name = name
        self.level = lookup_level(level)

    def debug(self, *args):
        """
        trivial debug impl
        """
        if self.level <= lookup_level("debug"):
            print "DEBUG | {} |".format(self.name), " ".join(args)

    def info(self, *args):
        """
        trivial info impl
        """
        if self.level <= lookup_level("info"):
            print "INFO  | {} |".format(self.name), " ".join(args)

    def warn(self, *args):
        """
        trivial warn impl
        """
        if self.level <= lookup_level("warn"):
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


class EnvColorLogger(BaseLogger):
    """
    Colored logger implementation. Like Logger but in color. Adds ability
    to look up minimum logging level from env using LOGGING_LEVEL env var.
    """
    def __init__(self, name, level=os.environ.get("LOGGING_LEVEL", "debug")):
        """
        set the name
        """
        self.name = name
        self.level = lookup_level(level)

    def debug(self, *args):
        """
        trivial debug impl
        """
        if self.level <= lookup_level("debug"):
            with ColorCM(printit, "blue") as colorm:
                colorm("DEBUG | {} |".format(self.name), *args)

    def info(self, *args):
        """
        trivial info impl
        """
        if self.level <= lookup_level("info"):
            with ColorCM(printit, "green") as colorm:
                colorm("INFO  | {} |".format(self.name), " ".join(args))

    def warn(self, *args):
        """
        trivial warn impl
        """
        if self.level <= lookup_level("warn"):
            with ColorCM(printit, "red") as colorm:
                colorm("WARN  | {} |".format(self.name), " ".join(args))

