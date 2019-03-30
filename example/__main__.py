from example.context import service_locator
from example.services import Logger, Dioculator

service_locator.register("logger", Logger)
service_locator.register("dioculator", Dioculator)

from example.bla import Bla

if __name__ == "__main__":
    bla = Bla()
    bla.talk()
