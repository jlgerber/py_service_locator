from example.context import service_locator
from example.services import Logger, Dioculator
from example.bla import Bla

service_locator.register("logger", Logger)
service_locator.register("dioculator", Dioculator)


if __name__ == "__main__":
    bla = Bla()
    bla.talk()
