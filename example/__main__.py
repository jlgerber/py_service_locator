from example.context import service_locator
from example.services import Logger, Dioculator
from example.services import BaseDioculator, BaseLogger

from example.bla import Bla

service_locator.key_is_superclass()
service_locator.register(BaseLogger, Logger)
service_locator.register(BaseDioculator, Dioculator)


if __name__ == "__main__":
    bla = Bla()
    bla.talk()
