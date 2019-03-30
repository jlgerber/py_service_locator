"""
SERVICE_LOCATOR

Implements this IoC pattern in Python. ServiceLocator is an alternative to
DependencyInjection, which is often achieved through passing dependencies down the
call graph via class inits. This can become unweildy for sufficiently large
or deeply nested code bases.

Rather than force classes to participate in dependency transport, we rely on
a service locator to store services instantiated up front, and a service locator
retrieval mechanism to fetch them from the service locator closer to the call sites.

This module draws inspiration from Python's logging module, creating a singleton
ServiceLocator instance in the module and providing convenience functions for
communicating with it.

Interactions with the ServiceLocator instance should be threadsafe by default.
"""

# disable 'redifined-outer-name' because it is ok in this case
# pylint: disable=W0621
# disable 'too-few-pubic-methods' because it doesnt make sense here
# pylint: disable=R0903

import inspect
try:
    import thread
    import threading
except ImportError:
    thread = None


__all__ = (
    "get_service",
    "register",
    "services",
    "get_service_proxy",
    "key_is_superclass"
)

#
#_LOCK is used to serialize access to shared data structures in this module.
# This is borrowed from python logging
#
if thread:
    _LOCK = threading.RLock()
else:
    _LOCK = None

def _acquire_lock():
    """
    Acquire the module-level lock for serializing access to shared data.

    This should be released with _release_lock().
    """
    if _LOCK:
        _LOCK.acquire()

def _release_lock():
    """
    Release the module-level lock acquired by calling _acquire_lock().
    """
    if _LOCK:
        _LOCK.release()

class LockCM(object):
    """
    Context Manager for creating a threading lock
    """
    def __enter__(self):
        _acquire_lock()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        _release_lock()


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
        self.key_is_superclass = key_is_superclass

    def register(self, key, service):
        """
        Register a service with the ServiceLocator.

        Parameters
        ----------
        key : Hashable
            The key under which one whishes to register the supplied `service`. The
            only restriction is that the key must be hashable, athough it is typically
            a string. Alternatively, if `key_is_superclass()` has been invoked during setup,
            one expects a superclass of the service, and ideally an abstract class at that.

        Raises
        ------
        AssertionError
            If `key_is_superclass()` has been invoked, and the service is not
            either an instance or subclass of `key`.
        TypeError
            If the key supplied is not hashable.
        """
        with LockCM() as lock:
            if self.key_is_superclass:
                if inspect.isclass(service):
                    assert issubclass(service, key)
                else:
                    assert isinstance(service, key)
            ServiceLocator._services[key] = service
        # try:
        #     _acquire_lock()
        #     if self.key_is_superclass:
        #         if inspect.isclass(service):
        #             assert issubclass(service, key)
        #         else:
        #             assert isinstance(service, key)
        #     ServiceLocator._services[key] = service
        # finally:
        #     _release_lock()

    @classmethod
    def has_service(cls, service_key):
        """
        Tests whether the ServiceLocator has the specified `service_key`.

        Parameters
        ----------
        service_key : Hashable
            The key we wish to test the ServiceLocator against. If the ServiceLocator
            has the supplied `service_key`, this method returns `True`. Otherwise, it
            returns `False`.

        Raises
        ------
        TypeError
            If `service_key` is unhashable.
        """
        with LockCM() as lock:
            return cls._services.has_key(service_key)
        # try:
        #     _acquire_lock()
        #     return cls._services.has_key(service_key)
        # finally:
        #     _release_lock()

    @classmethod
    def service(cls, service_key):
        """
        Given a potential service key, return the service associated with it.

        Parameters
        ----------
        service_key : Hashable
            The key which we wish to lookup a service with.

        Returns
        -------
        Service
            The previously registered service associated with the supplied `service_key`.

        Raises
        ------
        KeyError
            If no service is associated with the supplied `service_key`
        TypeError
            If the supplied `service_key` is unhashable
        """
        with LockCM() as lock:
            return cls._services[service_key]
        # try:
        #     _acquire_lock()
        #     return cls._services[service_key]
        # finally:
        #     _release_lock()


    @classmethod
    def services(cls):
        """
        Return a list of keys for registered services.

        Parameters
        ----------
        None

        Returns
        -------
        [ Hashable,... ]
            Shallow copy of the list of registered service keys.
        """
        with LockCM() as lock:
            return cls._services.keys()[:]
        # try:
        #     _acquire_lock()
        #     return cls._services.keys()[:]
        # finally:
        #     _release_lock()


SERVICE_LOCATOR = ServiceLocator()

class ServiceProxy(object):
    """
    A ServiceProxy captures a service request but does not
    fetch the service until invoked. This allows the service
    registration to take place after importing code which calls
    get_service_proxy, making usage more ergonomic at the cost of
    a slight runtime penalty.
    This class should handle proxied instances as well as classes
    """
    def __init__(self, service_key):
        """
        Initialize a ServiceProxy with a service. The ServiceProxy's job is to
        defer reification of the proxied service until first use. This is primarily
        to make importing ServiceProxy consumers order independent from service
        registry.

        Parameters
        ----------
        service_key : Hashable
            The key expected to be registered with the ServiceLocator. This may be
            any hashable object, although typically, one expects either a string or
            an abstract class, depending upon the ServiceLocator setup.
        """
        self._service_key = service_key
        self._service = None
        self._args = []
        self._kwargs = {}

    def __call__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        return self

    def __getattr__(self, name):
        if self._service is None:
            self._service = get_service(self._service_key)
            if inspect.isclass(self._service):
                self._service = self._service(*self._args, **self._kwargs)
                # dont want to hang on to references and prevent
                # garbage collection
                del self._args
                del self._kwargs
        return getattr(self._service, name)

def get_service_proxy(service_key):
    """
    Retrieve a ServiceProxy instance which defers retrieval of the requested
    service until first use.

    Parameters
    ----------
    service_key : Hashable
        Retrieve a service associated with the supplied service key. This can
        be any hashable object, but will typically be a string or class,
        depending on whether or not key_is_superclass() has been invoked during set.

    Returns
    -------
    service
        The service associated with the service_key, wrapped in a ServiceProxy.
        The wrapped service may be an instance or class. Both are supported by
        the ServiceProxy.

    Raises
    ------
    KeyError
        If a non-extant service_key is supplied
    """
    return ServiceProxy(service_key)

def get_service(service_key):
    """
    Retrieve a service. This call returns the service directly. The
    calling code should be imported after service registration. For
    this reason, we also provide get_service_proxy, which does not
    have this limitation.

    Parameters
    ----------
    service_key : Hashable
        Retrieve a service associated with the supplied service key. This can
        be any hashable object, but will typically be a string or class,
        depending on whether or not key_is_superclass() has been invoked during set.

    Returns
    -------
    service
        The service associated with the service_key. This may be an instance
        or class. Both are supported

    Raises
    ------
    KeyError
        If a non-extant service_key is supplied
    """
    return SERVICE_LOCATOR.service(service_key)


def services():
    """
    Return a list of keys for registered services.

    Parameters
    ----------
    None

    Returns
    -------
    [ Hashable,... ]
        Shallow copy of the list of registered service keys.
    """
    return SERVICE_LOCATOR.services()

def register(key, service):
    """
    Register a `service` with the ServiceLocator with the associated `key`.

    Parameters
    ----------
    key : Hashable
        The key under which one whishes to register the supplied `service`. The
        only restriction is that the key must be hashable, athough it is typically
        a string. Alternatively, if `key_is_superclass()` has been invoked during setup,
        one expects a superclass of the service, and ideally an abstract class at that.

    Raises
    ------
    AssertionError
        if `key_is_superclass()` has been invoked, and the service is not
        either an instance or subclass of `key`.
    TypeError
        If the key supplied is not hashable.
    """
    SERVICE_LOCATOR.register(key, service)

def key_is_superclass(value=True):
    """
    Configure the ServiceLocator to expect service keys to be superclasses of
    their registered services. Note: Invoccation of this function does not affect
    previously registered services.

    Parameters
    ----------
    value : bool
        Set the state to be True or False. By default, `value` defaults to True.
    """
    SERVICE_LOCATOR.key_is_superclass = value
