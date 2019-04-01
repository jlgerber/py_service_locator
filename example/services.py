"""
services

Abstract base classes followed by example implementations
"""
from abc import (ABCMeta, abstractmethod)

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


class Dioculator(BaseDioculator):
    """
    trivial dioculator impl
    """
    def __init__(self, frombulator):
        """
        initialize dioculator with frombulator. Note: we do not
        validate frombulator
        """
        self.frombulator = frombulator

    def dioculate(self):
        """
        dioculate interface impl
        """
        print "Dioculating with frombulator: '{}'".format(self.frombulator)
