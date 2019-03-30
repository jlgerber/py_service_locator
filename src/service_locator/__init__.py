__all__ = (
    "get_service",
    "register",
    "services",
    "get_service_proxy",
    "key_is_superclass"
)

import inspect

try:
    import thread
    import threading
except ImportError:
    thread = None

#
#_lock is used to serialize access to shared data structures in this module.
# This is borrowed from python logging
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
    """
    Class which tracks services. A service may be a python instance
    or class.
    """
    _services = {}
    def __init__(self, key_is_superclass=False):
        """
        If key_is_superclass is True, then we require the key to be
        the superclass of the service. This promotes SOLID design
        by requiring the dependence on an interface for a service
        """
        self._key_is_superclass = key_is_superclass

    def register(self, key, service):
        """
        Register a service.
        """
        try:
            _acquireLock()
            if self._key_is_superclass:
                if inspect.isclass(service):
                    assert issubclass(service, key)
                else:
                    assert isinstance(service, key)
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

class ServiceProxy(object):
    """
    A ServiceProxy captures a service request but does not
    fetch the service until invoked. This allows the service
    registration to take place after importing code which calls
    get_service_proxy, making usage more ergonomic at the cost of
    a slight runtime penalty.
    This class should handle proxied instances as well as classes
    """
    def __init__(self, service):
        self._service_name = service
        self._service = None
        self._args = []
        self._kwargs = {}

    def __call__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        return self

    def __getattr__(self, name):
        if self._service is None:
            self._service = get_service(self._service_name)
            if inspect.isclass(self._service):
                self._service = self._service(*self._args, **self._kwargs)
                # dont want to hang on to references and prevent
                # garbage collection
                del self._args
                del self._kwargs
        return getattr(self._service, name)

def get_service_proxy(service):
    """
    Retrieve a proxy
    """
    return ServiceProxy(service)

def get_service(service):
    """
    retrieve a service. This call returns the service directly. The
    calling code should be imported after service registration. For
    this reason, we also provide get_service_proxy, which does not
    have this limitation.
    """
    return service_locator.service(service)


def services():
    """
    Return a list of keys for registered services
    """
    return service_locator.services()

def register(key, service):
    service_locator.register(key, service)

def key_is_superclass():
    service_locator._key_is_superclass = True