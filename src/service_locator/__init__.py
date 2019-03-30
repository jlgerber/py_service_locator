__all__ = ("service_locator", "get_service", "register", "services")
try:
    import thread
    import threading
except ImportError:
    thread = None



#---------------------------------------------------------------------------
#   Thread-related stuff
#---------------------------------------------------------------------------

#
#_lock is used to serialize access to shared data structures in this module.
#This needs to be an RLock because fileConfig() creates and configures
#Handlers, and so might arbitrary user threads. Since Handler code updates the
#shared dictionary _handlers, it needs to acquire the lock. But if configuring,
#the lock would already have been acquired - so we need an RLock.
#The same argument applies to Loggers and Manager.loggerDict.
#
if thread:
    _lock = threading.RLock()
else:
    _lock = None

def _acquireLock():
    """
    Acquire the module-level lock for serializing access to shared data.

    This should be released with _releaseLock().
    """
    if _lock:
        _lock.acquire()

def _releaseLock():
    """
    Release the module-level lock acquired by calling _acquireLock().
    """
    if _lock:
        _lock.release()

class ServiceLocator(object):
    _services = {}

    def register(self, key, service):
        """
        Register service
        """
        try:
            _acquireLock()
            ServiceLocator._services[key] = service
        finally:
            _releaseLock()

    def has_service(self, key):
        return ServiceLocator._services.has_service(key)

    def service(self, key):
        try:
            _acquireLock()
            return ServiceLocator._services[key]
        finally:
            _releaseLock()

    def services(self):
        return ServiceLocator._services.keys()

service_locator = ServiceLocator()

def get_service(service):
    """
    retrieve a service
    """
    try:
        _acquireLock()
        return service_locator.service(service)
    finally:
        _releaseLock()

def services():
    return service_locator.services()

def register(key, service):
    service_locator.register(key, service)