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

# configure the service_locator to expect service_keys
# to be superclasses of registered services
service_locator.key_is_superclass()
# register some services
# try commenting out one or the other
service_locator.register(BaseLogger, Logger)
service_locator.register(BaseDioculator, Dioculator)

def validate():
    missing = service_locator.unbound_services()
    if len(missing) > 0:
        import sys
        print "ERROR: failed to configure all required services. Missing bindings:"
        for binding in missing:
            print "\t",binding
        sys.exit()

validate()
def main():
    """
    entry point for exe
    """

    bla = Bla()
    bla.talk()

if __name__ == "__main__":
    main()
