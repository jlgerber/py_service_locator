from abc import ABCMeta, abstractmethod

class BaseLogger:
    """
    ABC Logger class which defines a minimal logging
    interface
    """
    __meta__ = ABCMeta

    @abstractmethod
    def debug(self, *args):
        pass
    @abstractmethod
    def info(self, *kwargs):
        pass

    @abstractmethod
    def warn(self, *kwargs):
        pass


class BaseDioculator:
    """
    ABC Dioculator class which provides base class behavior
    """
    __meta__ = ABCMeta

    @abstractmethod
    def dioculate(self):
        pass


class Logger(BaseLogger):
    def __init__(self, name):
        self.name = name

    def debug(self, *args):
        print "DEBUG: {}:".format(self.name)," ".join(args)

    def info(self, *args):
        print "INFO: {}:".format(self.name)," ".join(args)

    def warn(self, *args):
        print "WARN: {}:".format(self.name)," ".join(args)


class Dioculator(BaseDioculator):
    def __init__(self, frombulator):
        self.frombulator = frombulator

    def dioculate(self):
        print "Dioculating with frombulator: '{}'".format(self.frombulator)
