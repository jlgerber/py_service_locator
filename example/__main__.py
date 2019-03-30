"""
__main__.py

import resources and invoke main function
"""
from example.context import service_locator
from example.services import (
    Logger,
    Dioculator,
    BaseDioculator,
    BaseLogger
)

from example.bla import Bla

service_locator.key_is_superclass()
service_locator.register(BaseLogger, Logger)
service_locator.register(BaseDioculator, Dioculator)

def main():
    """
    entry point for exe
    """
    bla = Bla()
    bla.talk()

if __name__ == "__main__":
    main()
