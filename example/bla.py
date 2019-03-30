from example.context import service_locator
from example.services import BaseDioculator, BaseLogger

cls = service_locator.get_service_proxy(BaseLogger)
logger = cls(__name__)


class Bla(object):
    dioculator = service_locator.get_service_proxy(BaseDioculator)("frombulator")

    def __init__(self):
        self.bla = "BLA"

    def talk(self):
        logger.info("about to talk")
        print self.bla
        self.dioculator.dioculate()
        logger.warn("just got done talking")
