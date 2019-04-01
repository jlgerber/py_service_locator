"""
__main__.py

import resources and invoke main function
"""
from example.context import service_locator
from example.services import (
    BaseDioculator,
    BaseFrombulator,
    BaseLogger
)
from example.dioculator import Dioculator
from example.frombulator import Frombulator
from example.logger import (ColorLogger, Logger, EnvColorLogger, EnvLogger)
from example.bla import Bla

# configure the service_locator to expect service_keys
# to be superclasses of registered services
service_locator.configure(
    key_is_superclass=True,
    allow_instances=False
)
# register some services
# try commenting out one or the other
service_locator.register(BaseLogger, EnvColorLogger)
# alternative to ColorLogger
#service_locator.register(BaseLogger, Logger)
# example mistake
#service_locator.register(BaseLogger, Dioculator)

service_locator.register(BaseDioculator, Dioculator)
service_locator.register(BaseFrombulator, Frombulator)

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
