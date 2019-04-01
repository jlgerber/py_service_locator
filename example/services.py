"""
services

Abstract base classes followed by example implementations
"""
from abc import (ABCMeta, abstractmethod)


__all__ = (
    "BaseLogger",
    "BaseDioculator",
    "BaseFrombulator",
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
    """
    Base Frombulator class
    """
    __meta__ = ABCMeta

    def __init__(self, frombulator):
        """
        initialize the Frombulator with a frombulator
        """
        self.frombulator = frombulator

    @abstractmethod
    def name(self):
        """
        Retrieve the name of the frombulator
        """
        pass

    @abstractmethod
    def frombulate(self):
        """frobulate"""
        pass
