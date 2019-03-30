from abc import ABCMeta, abstractmethod

class BaseLogger:
    __meta__ = ABCMeta

@abstractmethod
def debug(self, *args):
    raise NotImplementedError()

@abstractmethod
def info(self, *kwargs):
    raise NotImplementedError()

@abstractmethod
def warn(self, *kwargs):
    raise NotImplementedError()


class Logger(BaseLogger):
    def __init__(self, name):
        self.name = name

    def debug(self, *args):
        print "DEBUG: {}:".format(self.name)," ".join(args)

    def info(self, *args):
        print "INFO: {}:".format(self.name)," ".join(args)

    def warn(self, *args):
        print "WARN: {}:".format(self.name)," ".join(args)

class BaseDioculator:
    __meta__ = ABCMeta

@abstractmethod
def dioculate(self):
    raise NotImplementedError()

class Dioculator(BaseDioculator):
    def __init__(self, frombulator):
        self.frombulator = frombulator

    def dioculate(self):
        print "Dioculating with frombulator: '{}'".format(self.frombulator)
