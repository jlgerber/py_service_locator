
"""
dioculate.py

Standard dioculation implementation.
"""
from example.context import service_locator
from example.services import (BaseLogger, BaseFrombulator, BaseDioculator)

LOGGER = service_locator.get_service_proxy(BaseLogger, __name__)(__name__)

__all__ = ("Dioculator",)

class Dioculator(BaseDioculator):
    """
    Patterned after the initial Dioculator implementation from Q Division, before
    they started experimenting with unsound methodologies. Not quite the
    undergraduate variety, but doesn't require a PHD to follow.
    """
    frombulator_cls = service_locator.get_service_proxy(
        service_key=BaseFrombulator,
        bindee=".".join((__name__, "Dioculator"))
    )

    def __init__(self, frombulator):
        """
        Initialize Dioculator with Frombulator. Note: we do not
        validate frombulator
        """
        LOGGER.info("Dioculator initialized")
        self.frombulator = self.__class__.frombulator_cls(frombulator)

    def dioculate(self):
        """
        This does exactly what it says. Dioculates. As advertised. Cant ask for more eh?
        """
        LOGGER.info("Dioculator.dioculate()")
        print "Dioculating with frombulator: '{}'".format(self.frombulator.name())
