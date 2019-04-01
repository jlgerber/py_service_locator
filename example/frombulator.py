
"""
frombulator.py

Frombulator implementation.
"""
from example.context import service_locator
from example.services import (BaseLogger, BaseFrombulator)

LOGGER = service_locator.get_service_proxy(BaseLogger, __name__)(__name__)

__all__ = ("Frombulator",)


class Frombulator(BaseFrombulator):
    """
    A classic Mark II Frobulator. Nothing fancy mind you, but
    more reliable than the Frombulator2000 that came after it.
    """
    def __init__(self, name=None):
        """
        Initialize the Frombulator with an optional name, and stand back.
        We don't a repeat of '17 eh? Our insurance costs would go through the roof.
        """
        name = name or "myfrombulator"
        super(Frombulator, self).__init__(name)
        LOGGER.info("Frombulator initialized")

    def frombulate(self):
        """
        A sterling implementation of frombulation. Textbook really. Powerful, economical,
        but with a strong aesthetic sensibility.
        """
        LOGGER.info("calling Frombulator.frombulate()")
        print "frombulating with {}".format(self.frombulator)

    def name(self):
        """
        Cant have a Frombulator implementation without being able to get the name.
        We don't want another disaster like we got with the Lambulator, eh?
        """
        LOGGER.debug("calling Frombulator.name()")
        return self.frombulator
