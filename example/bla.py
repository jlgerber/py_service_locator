"""
example service locator usage.
"""
from example.context import service_locator
from example.services import BaseDioculator, BaseLogger

LOGGER_CLS = service_locator.get_service_proxy(BaseLogger, __name__)
LOGGER = LOGGER_CLS(__name__)


class Bla(object):
    """
    Class which uses the BaseDioculator service. While python does not provide
    interfaces, we can instruct service_locator to expect keys to be superclasses
    of registered services, thus establishing a contract for behavior.
    """
    dioculator = service_locator.get_service_proxy(BaseDioculator, 'Bla')("frombulator")

    def __init__(self):
        """
        Initialize a meaningless instance variable
        """
        self.bla = "BLA"

    def talk(self):
        """
        method which makes use of two services fetched from the service_locator:
        BaseLogger and BaseDioculator.
        """
        LOGGER.info("about to talk")
        print "Bla here. I just wanted to say '{}'".format(self.bla)
        self.dioculator.dioculate()
        LOGGER.warn("just got done talking")
