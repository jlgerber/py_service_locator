"""
services

Abstract base classes followed by example implementations
"""
from abc import (ABCMeta, abstractmethod)
from example.context import service_locator
from example.color_util import (ColorCM, printit)

__all__ = (
    "BaseLogger",
    "BaseDioculator",
    "BaseFrombulator",
    "Logger",
    "ColorLogger",
    "Dioculator",
    "Frombulator"
)

class BaseLogger(object):
    """
    ABC Logger class which defines a minimal logging
    interface
    """
    __meta__ = ABCMeta

    @abstractmethod
    def debug(self, *args):
        """debug"""
        pass

    @abstractmethod
    def info(self, *kwargs):
        """info"""
        pass

    @abstractmethod
    def warn(self, *kwargs):
        """warn"""
        pass


class BaseDioculator(object):
    """
    ABC Dioculator class which provides base class behavior
    """
    __meta__ = ABCMeta

    @abstractmethod
    def dioculate(self):
        """dioculate"""
        pass


class BaseFrombulator(object):
    __meta__ = ABCMeta

    def __init__(self, frombulator):
        self.frombulator = frombulator

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def frombulate(self):
        """frobulate"""
        pass

class Frombulator(BaseFrombulator):
    def __init__(self, name):
        name = name or "myfrombulator"
        super(Frombulator, self).__init__(name)

    def frombulate(self):
        print "frombulating with {}".format(self.frombulator)

    def name(self):
        return self.frombulator

class Logger(BaseLogger):
    """
    BaseLogger implementation
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
        print "INFO | {} |".format(self.name), " ".join(args)

    def warn(self, *args):
        """
        trivial warn impl
        """
        print "WARN | {} |".format(self.name), " ".join(args)


class ColorLogger(BaseLogger):
    """
    BaseLogger implementation
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
            colorm("INFO | {} |".format(self.name), " ".join(args))

    def warn(self, *args):
        """
        trivial warn impl
        """
        with ColorCM(printit, "red") as colorm:
            colorm("WARN | {} |".format(self.name), " ".join(args))


class Dioculator(BaseDioculator):
    """
    trivial dioculator impl
    """
    _frombulator_cls = service_locator.get_service_proxy(BaseFrombulator, "Dioculator")

    def __init__(self, frombulator):
        """
        initialize dioculator with frombulator. Note: we do not
        validate frombulator
        """
        self.frombulator = self.__class__._frombulator_cls(frombulator)

    def dioculate(self):
        """
        dioculate interface impl
        """
        print "Dioculating with frombulator: '{}'".format(self.frombulator.name())
